#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKAGE_VERSION = "4.0.0-alpha.3"
RECEIPT_SCHEMA = "cpt-install-receipt-v1"
KERNEL_BEGIN = "<!-- CPT-OS KERNEL BEGIN -->"
KERNEL_END = "<!-- CPT-OS KERNEL END -->"
EXCLUDE_BEGIN = "# CPT-OS BEGIN"
EXCLUDE_END = "# CPT-OS END"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def payload_root() -> Path:
    return package_root() / "payload"


def scaffold_root() -> Path:
    return payload_root() / "repo-scaffold"


def core_plugin_root() -> Path:
    return payload_root() / "marketplace-root" / "plugins" / "cpt-core"


def bundled_pack_root(name: str) -> Path:
    return package_root() / "domain-packs" / name


def pack_catalog_data() -> dict[str, Any]:
    return read_json(package_root() / "domain-packs" / "PACK_CATALOG.json", {}) or {}


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    atomic_write(path, text)


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def remove_empty_parents(path: Path, stop: Path) -> None:
    cur = path
    while cur != stop and cur.exists():
        try:
            cur.rmdir()
        except OSError:
            break
        cur = cur.parent


def git_root(project: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(project), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=True,
        )
        return Path(result.stdout.strip()).resolve()
    except (OSError, subprocess.CalledProcessError):
        return None


def git_tracked(project: Path, path: str) -> bool:
    try:
        subprocess.run(
            ["git", "-C", str(project), "ls-files", "--error-unmatch", path],
            text=True,
            capture_output=True,
            check=True,
        )
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def replace_marked_block(text: str, begin: str, end: str, block: str | None) -> tuple[str, bool]:
    pattern = re.compile(rf"(?:\n?){re.escape(begin)}.*?{re.escape(end)}(?:\n?)", re.S)
    found = bool(pattern.search(text))
    text = pattern.sub("\n", text)
    text = text.strip("\n")
    if block is not None:
        if text:
            text += "\n\n"
        text += block.strip("\n")
    if text:
        text += "\n"
    return text, found


def kernel_block() -> str:
    text = (scaffold_root() / "AGENTS.md").read_text(encoding="utf-8").strip()
    if KERNEL_BEGIN not in text or KERNEL_END not in text:
        raise RuntimeError("Payload AGENTS.md is missing managed markers")
    return text


def exclude_block(paths: list[str]) -> str:
    lines = [EXCLUDE_BEGIN, "# Local CPT OS runtime and plugin exposure"]
    lines.extend(paths)
    lines.append(EXCLUDE_END)
    return "\n".join(lines)


def update_exclude(project: Path, paths: list[str] | None) -> bool:
    root = git_root(project)
    if root is None:
        return False
    git_path = root / ".git"
    if git_path.is_file():
        content = git_path.read_text(encoding="utf-8").strip()
        if content.startswith("gitdir:"):
            git_dir = (root / content.split(":", 1)[1].strip()).resolve()
        else:
            return False
    else:
        git_dir = git_path
    exclude = git_dir / "info" / "exclude"
    old = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    block = exclude_block(paths) if paths else None
    new, _ = replace_marked_block(old, EXCLUDE_BEGIN, EXCLUDE_END, block)
    if new != old:
        atomic_write(exclude, new)
    return True


def load_receipt(project: Path) -> dict[str, Any]:
    path = project / ".cpt" / "install.json"
    data = read_json(path)
    if not isinstance(data, dict) or data.get("schema") != RECEIPT_SCHEMA:
        raise RuntimeError("No valid CPT installation receipt found")
    return data


def save_receipt(project: Path, receipt: dict[str, Any]) -> None:
    receipt["updated_at"] = now()
    write_json(project / ".cpt" / "install.json", receipt)


def default_receipt(mode: str, plugin_scope: str) -> dict[str, Any]:
    return {
        "schema": RECEIPT_SCHEMA,
        "package": "codex-product-os",
        "version": PACKAGE_VERSION,
        "mode": mode,
        "plugin_scope": plugin_scope,
        "created_at": now(),
        "updated_at": now(),
        "managed_files": {},
        "mutable_files": [],
        "agents": {},
        "plugin": {},
        "packs": [],
        "warnings": [],
    }


def register_managed(receipt: dict[str, Any], project: Path, path: Path, created: bool, mutable: bool = False) -> None:
    key = rel(path, project)
    if mutable:
        if key not in receipt["mutable_files"]:
            receipt["mutable_files"].append(key)
        return
    receipt["managed_files"][key] = {
        "sha256": sha256(path),
        "created": created,
    }


def copy_initial(project: Path, receipt: dict[str, Any], src_rel: str, dst_rel: str, mutable: bool = False) -> None:
    src = scaffold_root() / src_rel
    dst = project / dst_rel
    created = not dst.exists()
    if not dst.exists():
        copy_file(src, dst)
    register_managed(receipt, project, dst, created=created, mutable=mutable)


def sharing_mode_name(mode: str) -> str:
    return "local_ignored" if mode == "local" else "team_shared"


def patch_runtime_mode(project: Path, mode: str) -> None:
    runtime = project / ".cpt" / "runtime.yaml"
    text = runtime.read_text(encoding="utf-8")
    text = re.sub(r"^sharing_mode:\s*\S+\s*$", f"sharing_mode: {sharing_mode_name(mode)}", text, flags=re.M)
    text = re.sub(r"^updated_at:.*$", f"updated_at: '{now()}'", text, flags=re.M)
    atomic_write(runtime, text)


def is_only_kernel_block(text: str) -> bool:
    stripped, _ = replace_marked_block(text, KERNEL_BEGIN, KERNEL_END, None)
    return not stripped.strip()


def install_agents(project: Path, receipt: dict[str, Any], mode: str, policy: str, allow_tracked_change: bool) -> tuple[str, bool]:
    path = project / "AGENTS.md"
    block = kernel_block()
    tracked = git_tracked(project, "AGENTS.md") if git_root(project) else False
    exists = path.exists()
    current = path.read_text(encoding="utf-8") if exists else ""
    has_marker = KERNEL_BEGIN in current and KERNEL_END in current

    effective = policy
    if policy == "auto":
        if not exists:
            effective = "create"
        elif has_marker:
            effective = "merge"
        elif mode == "local" and tracked and not allow_tracked_change:
            effective = "skip"
        else:
            effective = "merge"

    if effective == "create":
        if exists and not has_marker:
            raise RuntimeError("AGENTS.md already exists; use --agents-policy merge or skip")
        atomic_write(path, block + "\n")
        result = "created"
        active = True
    elif effective == "merge":
        if mode == "local" and tracked and not allow_tracked_change:
            raise RuntimeError(
                "Refusing to modify tracked AGENTS.md in local mode. Use --agents-policy skip, "
                "team mode, or --allow-tracked-agents-change."
            )
        new, _ = replace_marked_block(current, KERNEL_BEGIN, KERNEL_END, block)
        atomic_write(path, new)
        result = "merged"
        active = True
    elif effective == "skip":
        snippet = project / ".cpt" / "AGENTS_SNIPPET.md"
        snippet_created = not snippet.exists()
        atomic_write(snippet, block + "\n")
        register_managed(receipt, project, snippet, created=snippet_created)
        result = "skipped_existing"
        active = has_marker
        receipt["warnings"].append(
            "Root AGENTS.md was not modified. CPT runtime is installed, but automatic kernel guidance "
            "is inactive until the managed snippet is merged or the plugin skill is invoked."
        )
    else:
        raise RuntimeError(f"Unknown agents policy: {effective}")

    receipt["agents"] = {
        "path": "AGENTS.md",
        "result": result,
        "tracked_before_install": tracked,
        "kernel_guidance_active": active,
    }
    if path.exists() and result in {"created", "merged"}:
        receipt["agents"]["sha256"] = sha256(path)
    return result, active


def marketplace_entry(name: str, source_path: str) -> dict[str, Any]:
    return {
        "name": name,
        "source": {"source": "local", "path": source_path},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }


def upsert_marketplace(path: Path, marketplace_name: str, entry: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    existed = path.exists()
    data = read_json(path, {})
    if not isinstance(data, dict):
        raise RuntimeError(f"Marketplace is not a JSON object: {path}")
    data.setdefault("name", marketplace_name)
    data.setdefault("interface", {"displayName": "CPT OS Plugins"})
    plugins = data.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise RuntimeError(f"Marketplace plugins must be a list: {path}")
    plugins[:] = [item for item in plugins if item.get("name") != entry["name"]]
    plugins.append(entry)
    plugins.sort(key=lambda item: item.get("name", ""))
    write_json(path, data)
    return existed, data


def remove_marketplace_entry(path: Path, name: str, remove_if_empty_and_created: bool = False) -> bool:
    if not path.exists():
        return False
    data = read_json(path, {})
    plugins = data.get("plugins", []) if isinstance(data, dict) else []
    before = len(plugins)
    plugins = [item for item in plugins if item.get("name") != name]
    if before == len(plugins):
        return False
    data["plugins"] = plugins
    if not plugins and remove_if_empty_and_created:
        path.unlink()
        remove_empty_parents(path.parent, path.parents[3] if len(path.parents) >= 4 else path.parent)
    else:
        write_json(path, data)
    return True


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()


def personal_marketplace() -> Path:
    return (Path.home() / ".agents" / "plugins" / "marketplace.json").resolve()


def install_core_plugin(project: Path, receipt: dict[str, Any], scope: str) -> None:
    if scope == "none":
        receipt["plugin"] = {"scope": "none", "status": "not_exposed"}
        return
    if scope == "personal":
        target = codex_home() / "plugins" / "cpt-core"
        copy_tree(core_plugin_root(), target)
        market = personal_marketplace()
        existed, _ = upsert_marketplace(
            market,
            "cpt-personal",
            marketplace_entry("cpt-core", "./.codex/plugins/cpt-core"),
        )
        receipt["plugin"] = {
            "scope": "personal",
            "plugin_path": str(target),
            "marketplace_path": str(market),
            "marketplace_existed": existed,
            "status": "exposed_not_enabled",
        }
        return
    if scope == "repo":
        target = project / "plugins" / "cpt-core"
        copy_tree(core_plugin_root(), target)
        market = project / ".agents" / "plugins" / "marketplace.json"
        existed, _ = upsert_marketplace(
            market,
            "cpt-repo",
            marketplace_entry("cpt-core", "./plugins/cpt-core"),
        )
        receipt["plugin"] = {
            "scope": "repo",
            "plugin_path": rel(target, project),
            "marketplace_path": rel(market, project),
            "marketplace_existed": existed,
            "status": "exposed_not_enabled",
        }
        for file in sorted(target.rglob("*")):
            if file.is_file():
                register_managed(receipt, project, file, created=True)
        register_managed(receipt, project, market, created=not existed)
        return
    raise RuntimeError(f"Unknown plugin scope: {scope}")


def core_scaffold_files() -> list[tuple[str, bool]]:
    return [
        (".cpt/runtime.yaml", True),
        (".cpt/current.yaml", True),
        (".cpt/task-index.yaml", True),
        (".cpt/runtime-summary.md", True),
        (".cpt/OPERATIONS.md", False),
        (".cpt/requirements.txt", False),
        (".cpt/bin/cpt_runtime.py", False),
        (".cpt/schema-bundle.json", False),
    ]


def install(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    project.mkdir(parents=True, exist_ok=True)
    receipt_path = project / ".cpt" / "install.json"
    if receipt_path.exists():
        if not args.force:
            raise RuntimeError("CPT is already installed. Use update or uninstall.")
        print("Existing CPT receipt found; --force delegates to a conflict-aware update.")
        return update(argparse.Namespace(project=str(project), force=True))

    plugin_scope = args.plugin_scope
    if plugin_scope == "auto":
        plugin_scope = "personal" if args.mode == "local" else "repo"
    receipt = default_receipt(args.mode, plugin_scope)

    for path in [
        project / ".cpt" / "tasks",
        project / ".cpt" / "micro-changes",
        project / ".cpt" / "leases",
        project / ".cpt" / "checkpoints",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    for file, mutable in core_scaffold_files():
        copy_initial(project, receipt, file, file, mutable=mutable)
    patch_runtime_mode(project, args.mode)

    agents_result, agents_active = install_agents(
        project,
        receipt,
        mode=args.mode,
        policy=args.agents_policy,
        allow_tracked_change=args.allow_tracked_agents_change,
    )
    install_core_plugin(project, receipt, plugin_scope)

    if args.mode == "local":
        ignore_paths = ["/.cpt/"]
        if agents_result in {"created", "merged"} and not git_tracked(project, "AGENTS.md"):
            ignore_paths.append("/AGENTS.md")
        if plugin_scope == "repo":
            ignore_paths += ["/.agents/plugins/marketplace.json", "/plugins/cpt-core/"]
        if not update_exclude(project, ignore_paths):
            receipt["warnings"].append(
                "Local mode requested, but no Git repository was detected. Runtime files are not automatically hidden from VCS."
            )
    else:
        update_exclude(project, None)

    save_receipt(project, receipt)
    print(f"CPT OS {PACKAGE_VERSION} installed in {project}")
    print(f"mode={args.mode}; plugin_scope={plugin_scope}; agents={agents_result}")
    if not agents_active:
        print("WARNING: automatic AGENTS kernel guidance is not active; see .cpt/AGENTS_SNIPPET.md")
    if plugin_scope != "none":
        print("Plugin is exposed through a marketplace. Restart Codex and install/enable CPT Core in the plugin UI.")
    if receipt["warnings"]:
        for warning in receipt["warnings"]:
            print(f"WARNING: {warning}")
    return 0


def managed_conflicts(project: Path, receipt: dict[str, Any]) -> list[str]:
    conflicts = []
    for path_str, meta in receipt.get("managed_files", {}).items():
        path = project / path_str
        if not path.exists():
            continue
        expected = meta.get("sha256")
        if expected and sha256(path) != expected:
            conflicts.append(path_str)
    return conflicts


def backup_paths(project: Path, paths: list[Path], label: str) -> Path:
    backup = project / ".cpt" / "backups" / f"{label}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    for path in paths:
        if not path.exists():
            continue
        try:
            relative = path.resolve().relative_to(project.resolve())
        except ValueError:
            relative = Path(path.name)
        dst = backup / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        if path.is_dir():
            shutil.copytree(path, dst)
        else:
            shutil.copy2(path, dst)
    return backup


def update(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    receipt = load_receipt(project)
    conflicts = managed_conflicts(project, receipt)
    if conflicts and not args.force:
        print("Refusing update because managed files changed:", file=sys.stderr)
        for item in conflicts:
            print(f"- {item}", file=sys.stderr)
        print("Re-run with --force to back up and replace managed tooling files.", file=sys.stderr)
        return 2
    if conflicts:
        backup = backup_paths(project, [project / item for item in conflicts], "update-conflicts")
        print(f"Backed up conflicts to {backup}")

    new_managed: dict[str, Any] = {}
    for file, mutable in core_scaffold_files():
        dst = project / file
        if mutable:
            continue
        copy_file(scaffold_root() / file, dst)
        new_managed[file] = {"sha256": sha256(dst), "created": receipt.get("managed_files", {}).get(file, {}).get("created", False)}
    receipt["managed_files"].update(new_managed)
    patch_runtime_mode(project, receipt["mode"])

    agents = receipt.get("agents", {})
    if agents.get("result") in {"created", "merged"} and (project / "AGENTS.md").exists():
        current = (project / "AGENTS.md").read_text(encoding="utf-8")
        new, _ = replace_marked_block(current, KERNEL_BEGIN, KERNEL_END, kernel_block())
        atomic_write(project / "AGENTS.md", new)
        agents["sha256"] = sha256(project / "AGENTS.md")
    elif (project / ".cpt" / "AGENTS_SNIPPET.md").exists():
        atomic_write(project / ".cpt" / "AGENTS_SNIPPET.md", kernel_block() + "\n")

    scope = receipt.get("plugin_scope", "none")
    install_core_plugin(project, receipt, scope)
    receipt["version"] = PACKAGE_VERSION
    save_receipt(project, receipt)
    print(f"CPT OS updated to {PACKAGE_VERSION}; mutable runtime state was preserved.")
    return 0


def backup_runtime_outside_project(project: Path, backup_dir: str | None) -> Path:
    if backup_dir:
        root = Path(backup_dir).expanduser().resolve()
    else:
        root = Path.home() / ".cpt-os" / "backups"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", project.name).strip("-") or "project"
    target = root / f"{slug}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(project / ".cpt", target / ".cpt")
    return target


def uninstall(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    receipt = load_receipt(project)

    if not args.discard_state and (project / ".cpt").exists():
        backup = backup_runtime_outside_project(project, args.backup_dir)
        print(f"Runtime state backed up to {backup}")

    agents_path = project / "AGENTS.md"
    if agents_path.exists():
        current = agents_path.read_text(encoding="utf-8")
        new, found = replace_marked_block(current, KERNEL_BEGIN, KERNEL_END, None)
        if found:
            if not new.strip():
                agents_path.unlink()
            else:
                atomic_write(agents_path, new)

    plugin = receipt.get("plugin", {})
    scope = plugin.get("scope", "none")
    if scope == "repo":
        path = project / plugin.get("plugin_path", "plugins/cpt-core")
        if path.exists():
            shutil.rmtree(path)
        market = project / plugin.get("marketplace_path", ".agents/plugins/marketplace.json")
        remove_marketplace_entry(market, "cpt-core", remove_if_empty_and_created=not plugin.get("marketplace_existed", True))
        remove_empty_parents(path.parent, project)
    elif scope == "personal" and args.remove_personal_plugin:
        path = Path(plugin.get("plugin_path", codex_home() / "plugins" / "cpt-core"))
        if path.exists():
            shutil.rmtree(path)
        market = Path(plugin.get("marketplace_path", personal_marketplace()))
        remove_marketplace_entry(market, "cpt-core", remove_if_empty_and_created=not plugin.get("marketplace_existed", True))

    update_exclude(project, None)
    if (project / ".cpt").exists():
        shutil.rmtree(project / ".cpt")
    print("CPT OS project scaffold removed. Application files were not touched.")
    if scope == "personal" and not args.remove_personal_plugin:
        print("Personal CPT Core plugin was left installed because it may be used by other projects.")
    return 0


def runtime_validate(project: Path) -> tuple[bool, str]:
    script = project / ".cpt" / "bin" / "cpt_runtime.py"
    if not script.exists():
        return False, "runtime CLI missing"
    result = subprocess.run(
        [sys.executable, str(script), "validate"],
        cwd=project,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def count_framework_files(project: Path, receipt: dict[str, Any]) -> int:
    paths = set(receipt.get("managed_files", {}).keys())
    paths.update(receipt.get("mutable_files", []))
    paths.add(".cpt/install.json")
    if receipt.get("agents", {}).get("result") in {"created", "merged"}:
        paths.add("AGENTS.md")
    return len(paths)


def status(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    receipt = load_receipt(project)
    ok, validation = runtime_validate(project)
    data = {
        "project": str(project),
        "version": receipt.get("version"),
        "mode": receipt.get("mode"),
        "plugin_scope": receipt.get("plugin_scope"),
        "agents": receipt.get("agents"),
        "framework_file_count": count_framework_files(project, receipt),
        "runtime_valid": ok,
        "runtime_validation": validation,
        "warnings": receipt.get("warnings", []),
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for key, value in data.items():
            print(f"{key}: {value}")
    return 0 if ok else 1


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise RuntimeError(f"Skill missing YAML frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise RuntimeError(f"Skill frontmatter is not closed: {path}")
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def validate_plugin(path: Path, require_pack: bool = True) -> dict[str, Any]:
    manifest_path = path / ".codex-plugin" / "plugin.json"
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise RuntimeError(f"Missing plugin manifest: {manifest_path}")
    for key in ["name", "version", "description"]:
        if not manifest.get(key):
            raise RuntimeError(f"Plugin manifest missing {key}: {manifest_path}")
    name = manifest["name"]
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise RuntimeError(f"Plugin name must be kebab-case: {name}")
    if require_pack:
        pack = read_json(path / "cpt-pack.json")
        if not isinstance(pack, dict) or pack.get("name") != name:
            raise RuntimeError(f"Missing or mismatched cpt-pack.json in {path}")
        if pack.get("schema_version") != "cpt-pack-v2":
            raise RuntimeError(f"Unsupported cpt-pack schema in {path}: {pack.get('schema_version')}")
    skills_dir = path / manifest.get("skills", "./skills/")
    skills = []
    if skills_dir.exists():
        for skill in sorted(skills_dir.glob("*/SKILL.md")):
            meta = parse_frontmatter(skill)
            if not meta.get("name") or not meta.get("description"):
                raise RuntimeError(f"Skill frontmatter missing name/description: {skill}")
            if meta.get("name") != skill.parent.name:
                raise RuntimeError(f"Skill name/path mismatch: {skill}")
            skills.append(meta)
    if require_pack:
        names = sorted(skill["name"] for skill in skills)
        if pack.get("skill_count") != len(skills):
            raise RuntimeError(
                f"cpt-pack.json skill_count={pack.get('skill_count')} does not match {len(skills)} skills in {path}"
            )
        if sorted(pack.get("skill_ids", [])) != names:
            raise RuntimeError(f"cpt-pack.json skill_ids do not match installed skills in {path}")
        legacy = pack.get("legacy_source")
        if not isinstance(legacy, dict) or not legacy.get("package") or not isinstance(legacy.get("skill_count"), int):
            raise RuntimeError(f"cpt-pack.json legacy_source is missing or invalid in {path}")
    return {"manifest": manifest, "skills": skills}


def metadata_budget_for_plugins(paths: list[Path]) -> dict[str, Any]:
    total = 0
    skills = []
    for plugin_path in paths:
        validated = validate_plugin(plugin_path, require_pack=False)
        plugin_name = validated["manifest"]["name"]
        for skill in validated["skills"]:
            entry = f"{skill['name']}\n{skill['description']}\n{plugin_name}/skills/{skill['name']}/SKILL.md"
            chars = len(entry)
            total += chars
            skills.append({"plugin": plugin_name, "name": skill["name"], "chars": chars})
    return {"skill_count": len(skills), "estimated_discovery_chars": total, "skills": skills}


def doctor(args: argparse.Namespace) -> int:
    project = Path(args.project).resolve()
    receipt = load_receipt(project)
    problems: list[str] = []
    warnings: list[str] = list(receipt.get("warnings", []))

    ok, validation = runtime_validate(project)
    if not ok:
        problems.append(validation)
    agents = receipt.get("agents", {})
    if not agents.get("kernel_guidance_active"):
        warnings.append("Automatic AGENTS kernel guidance is inactive")
    count = count_framework_files(project, receipt)
    if count >= 20:
        problems.append(f"Repo-local framework file count is {count}; expected < 20")

    scope = receipt.get("plugin_scope")
    plugin_paths: list[Path] = []
    if scope == "repo":
        plugin_path = project / receipt["plugin"]["plugin_path"]
        plugin_paths.append(plugin_path)
    elif scope == "personal":
        plugin_paths.append(Path(receipt["plugin"]["plugin_path"]))
    for plugin_path in plugin_paths:
        try:
            validate_plugin(plugin_path)
        except RuntimeError as exc:
            problems.append(str(exc))
    if plugin_paths:
        budget = metadata_budget_for_plugins(plugin_paths)
        if budget["estimated_discovery_chars"] > 8000:
            warnings.append(
                f"Active plugin metadata estimate is {budget['estimated_discovery_chars']} chars; review skill discovery budget"
            )

    print("DOCTOR")
    print(f"framework_files: {count}")
    print(f"runtime: {'PASS' if ok else 'FAIL'}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for problem in problems:
        print(f"ERROR: {problem}")
    return 0 if not problems else 1


def pack_add(args: argparse.Namespace) -> int:
    if getattr(args, "name", None):
        source = bundled_pack_root(args.name).resolve()
        if not source.exists():
            raise RuntimeError(f"Unknown bundled pack: {args.name}")
    else:
        source = Path(args.path).resolve()
    validated = validate_plugin(source)
    name = validated["manifest"]["name"]
    if name == "cpt-core":
        raise RuntimeError("Use install/update for cpt-core")
    project = Path(args.project).resolve() if args.project else None
    if args.scope == "repo":
        if project is None:
            raise RuntimeError("--project is required for repo pack scope")
        target = project / "plugins" / name
        market = project / ".agents" / "plugins" / "marketplace.json"
        source_path = f"./plugins/{name}"
        market_name = "cpt-repo"
    else:
        target = codex_home() / "plugins" / name
        market = personal_marketplace()
        source_path = f"./.codex/plugins/{name}"
        market_name = "cpt-personal"
    copy_tree(source, target)
    upsert_marketplace(market, market_name, marketplace_entry(name, source_path))
    if project and (project / ".cpt" / "install.json").exists():
        receipt = load_receipt(project)
        receipt["packs"] = [p for p in receipt.get("packs", []) if p.get("name") != name]
        receipt["packs"].append({"name": name, "scope": args.scope, "path": str(target), "status": "exposed_not_enabled"})
        save_receipt(project, receipt)
    print(f"Pack {name} exposed in {args.scope} marketplace. Enable it independently in Codex.")
    return 0


def pack_remove(args: argparse.Namespace) -> int:
    name = args.name
    project = Path(args.project).resolve() if args.project else None
    if args.scope == "repo":
        if project is None:
            raise RuntimeError("--project is required for repo pack scope")
        target = project / "plugins" / name
        market = project / ".agents" / "plugins" / "marketplace.json"
    else:
        target = codex_home() / "plugins" / name
        market = personal_marketplace()
    if target.exists():
        shutil.rmtree(target)
    remove_marketplace_entry(market, name)
    if project and (project / ".cpt" / "install.json").exists():
        receipt = load_receipt(project)
        receipt["packs"] = [p for p in receipt.get("packs", []) if p.get("name") != name]
        save_receipt(project, receipt)
    print(f"Pack {name} removed from {args.scope} marketplace. Other packs were preserved.")
    return 0


def pack_catalog(args: argparse.Namespace) -> int:
    data = pack_catalog_data()
    core = data.get("core", {})
    print(f"{core.get('name')}\t{core.get('status')}\t{core.get('skill_count')}")
    for pack in data.get("domains", []):
        print(f"{pack.get('id')}\t{pack.get('status')}\t{pack.get('skill_count')}")
    return 0


def pack_list(args: argparse.Namespace) -> int:
    if args.scope == "repo":
        if not args.project:
            raise RuntimeError("--project is required for repo pack scope")
        market = Path(args.project).resolve() / ".agents" / "plugins" / "marketplace.json"
    else:
        market = personal_marketplace()
    data = read_json(market, {}) or {}
    for plugin in data.get("plugins", []):
        print(f"{plugin.get('name')}\t{plugin.get('source', {}).get('path')}\t{plugin.get('policy', {}).get('installation')}")
    return 0


def skill_resolve(args: argparse.Namespace) -> int:
    migration = read_json(package_root() / "migration" / "SKILL_MIGRATION.json", {}) or {}
    registry = read_json(package_root() / "skills" / "SKILL_REGISTRY.json", {}) or {}
    by_source = {item.get("source_skill"): item for item in migration.get("mappings", [])}
    by_id = {item.get("id"): item for item in registry.get("skills", [])}
    item = by_source.get(args.name) or by_id.get(args.name)
    if not item:
        raise RuntimeError(f"Unknown legacy or active skill: {args.name}")
    target = item.get("target_skill") or item.get("id")
    active = by_id.get(target, {})
    result = {
        "query": args.name,
        "target_skill": target,
        "plugin": active.get("plugin") or item.get("target_plugin"),
        "implicit": active.get("implicit"),
        "description": active.get("description"),
        "migration_note": item.get("migration_note"),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['query']} -> {result['target_skill']} ({result['plugin']})")
        if result.get("migration_note"):
            print(result["migration_note"])
    return 0


def metadata(args: argparse.Namespace) -> int:
    paths = [Path(item).resolve() for item in args.plugin]
    result = metadata_budget_for_plugins(paths)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["estimated_discovery_chars"] <= args.max_chars else 2


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Install and manage Codex Product OS 4.0 distribution")
    sub = p.add_subparsers(dest="command", required=True)

    install_p = sub.add_parser("install")
    install_p.add_argument("--project", default=".")
    install_p.add_argument("--mode", choices=["local", "team"], default="local")
    install_p.add_argument("--plugin-scope", choices=["auto", "personal", "repo", "none"], default="auto")
    install_p.add_argument("--agents-policy", choices=["auto", "create", "merge", "skip"], default="auto")
    install_p.add_argument("--allow-tracked-agents-change", action="store_true")
    install_p.add_argument("--force", action="store_true")
    install_p.set_defaults(func=install)

    update_p = sub.add_parser("update")
    update_p.add_argument("--project", default=".")
    update_p.add_argument("--force", action="store_true")
    update_p.set_defaults(func=update)

    uninstall_p = sub.add_parser("uninstall")
    uninstall_p.add_argument("--project", default=".")
    uninstall_p.add_argument("--discard-state", action="store_true")
    uninstall_p.add_argument("--backup-dir")
    uninstall_p.add_argument("--remove-personal-plugin", action="store_true")
    uninstall_p.set_defaults(func=uninstall)

    status_p = sub.add_parser("status")
    status_p.add_argument("--project", default=".")
    status_p.add_argument("--json", action="store_true")
    status_p.set_defaults(func=status)

    doctor_p = sub.add_parser("doctor")
    doctor_p.add_argument("--project", default=".")
    doctor_p.set_defaults(func=doctor)

    add_p = sub.add_parser("pack-add")
    add_src = add_p.add_mutually_exclusive_group(required=True)
    add_src.add_argument("--path")
    add_src.add_argument("--name")
    add_p.add_argument("--scope", choices=["personal", "repo"], required=True)
    add_p.add_argument("--project")
    add_p.set_defaults(func=pack_add)

    remove_p = sub.add_parser("pack-remove")
    remove_p.add_argument("--name", required=True)
    remove_p.add_argument("--scope", choices=["personal", "repo"], required=True)
    remove_p.add_argument("--project")
    remove_p.set_defaults(func=pack_remove)

    catalog_p = sub.add_parser("pack-catalog")
    catalog_p.set_defaults(func=pack_catalog)

    resolve_p = sub.add_parser("skill-resolve")
    resolve_p.add_argument("--name", required=True)
    resolve_p.add_argument("--json", action="store_true")
    resolve_p.set_defaults(func=skill_resolve)

    list_p = sub.add_parser("pack-list")
    list_p.add_argument("--scope", choices=["personal", "repo"], required=True)
    list_p.add_argument("--project")
    list_p.set_defaults(func=pack_list)

    meta_p = sub.add_parser("metadata-budget")
    meta_p.add_argument("--plugin", action="append", required=True)
    meta_p.add_argument("--max-chars", type=int, default=8000)
    meta_p.set_defaults(func=metadata)

    return p


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
