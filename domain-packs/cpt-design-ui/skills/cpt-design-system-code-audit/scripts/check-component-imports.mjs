#!/usr/bin/env node
// Heuristic DS component contract scanner.
// Usage:
//   node scripts/check-component-imports.mjs [root]
//     [--manifest docs/design-system/DESIGN_SYSTEM_MANIFEST.json]
//     [--json]
//     [--fail-on-violation]
//     [--strict-ds]
//     [--fail-on-warning]
//
// Notes:
// - Normal mode: wrong component imports and duplicate DS component declarations are violations.
// - Strict DS mode: native primitives such as <button> / <input> become violations when matching DS components exist,
//   except inside files that belong to the DS source itself.
// - This is a heuristic scanner, not a substitute for visual QA, DS authority checks, or component review.

import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const flags = new Set(args.filter(a => a.startsWith('--')));
function optionValue(name, fallback) {
  const idx = args.indexOf(name);
  if (idx >= 0 && args[idx + 1] && !args[idx + 1].startsWith('--')) return args[idx + 1];
  return fallback;
}
function positionalArgs() {
  const out = [];
  for (let i = 0; i < args.length; i += 1) {
    const a = args[i];
    if (a === '--manifest') { i += 1; continue; }
    if (!a.startsWith('--')) out.push(a);
  }
  return out;
}

const root = positionalArgs()[0] || 'src';
const manifestPath = optionValue('--manifest', 'docs/design-system/DESIGN_SYSTEM_MANIFEST.json');
const asJson = flags.has('--json');
const failOnViolation = flags.has('--fail-on-violation');
const strictDs = flags.has('--strict-ds');
const failOnWarning = flags.has('--fail-on-warning');

const exts = new Set(['.ts', '.tsx', '.js', '.jsx']);
const ignoreDirs = new Set(['node_modules', '.git', 'dist', 'build', '.next', 'coverage', 'vendor']);

function normalizeAllowed(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v;
  return [v];
}

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      if (!ignoreDirs.has(ent.name)) out.push(...walk(p));
    } else if (ent.isFile() && exts.has(path.extname(ent.name))) {
      out.push(p);
    }
  }
  return out;
}

function lineNumber(text, index) {
  return text.slice(0, index).split(/\r?\n/).length;
}

function normalizePathLike(p) {
  return String(p || '')
    .replace(/^@\//, '')
    .replace(/^\.\//, '')
    .replace(/\\/g, '/')
    .replace(/\.(tsx|ts|jsx|js)$/i, '')
    .replace(/\/index$/i, '');
}

function importSourceMatches(source, allowed) {
  const ns = normalizePathLike(source);
  return allowed.some(a => {
    const na = normalizePathLike(a);
    return ns === na || ns.endsWith('/' + na) || na.endsWith('/' + ns) || ns.endsWith(na) || na.endsWith(ns);
  });
}

function fileBelongsToAllowedSource(file, allowed) {
  const nf = normalizePathLike(file.split(path.sep).join('/'));
  return allowed.some(a => {
    const na = normalizePathLike(a);
    return nf === na || nf.endsWith('/' + na) || nf.includes('/' + na + '/') || nf.endsWith(na);
  });
}

function sourceRootsFromManifest(manifest, allowedByComponent) {
  const roots = new Set();
  const explicit = manifest.ds_roots || manifest.design_system_roots || manifest.component_roots || [];
  for (const r of normalizeAllowed(explicit)) roots.add(normalizePathLike(r));
  for (const allowed of Object.values(allowedByComponent)) {
    for (const src of allowed) {
      const n = normalizePathLike(src);
      const parts = n.split('/').filter(Boolean);
      // For common aliases like components/ui/button, root becomes components/ui.
      if (parts.length > 1) roots.add(parts.slice(0, -1).join('/'));
      else if (parts.length === 1) roots.add(parts[0]);
    }
  }
  return [...roots].filter(Boolean);
}

function fileBelongsToDsSource(file, dsRoots, allowedByComponent) {
  const nf = normalizePathLike(file.split(path.sep).join('/'));
  for (const root of dsRoots) {
    if (nf.includes('/' + root + '/') || nf.endsWith('/' + root) || nf.startsWith(root + '/') || nf === root) return true;
  }
  for (const allowed of Object.values(allowedByComponent)) {
    if (fileBelongsToAllowedSource(file, allowed)) return true;
  }
  return false;
}

if (!fs.existsSync(manifestPath)) {
  const msg = `No DS manifest found at ${manifestPath}. Run design-recon/design-system-manifest first.`;
  const result = { manifestPath, root, strictDs, violations: [], warnings: [{ type: 'missing-manifest', message: msg }] };
  if (asJson) console.log(JSON.stringify(result, null, 2));
  else console.log(msg);
  if (strictDs && (failOnViolation || failOnWarning)) process.exit(1);
  process.exit(0);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const componentImports = manifest.component_imports || {};
const components = Object.keys(componentImports);
const allowedByComponent = Object.fromEntries(components.map(name => [name, normalizeAllowed(componentImports[name])]));
const dsRoots = sourceRootsFromManifest(manifest, allowedByComponent);
const files = walk(root);
const violations = [];
const warnings = [];

for (const file of files) {
  const text = fs.readFileSync(file, 'utf8');
  const inDsSource = fileBelongsToDsSource(file, dsRoots, allowedByComponent);

  // import { Button } from '...'; import Button from '...';
  const importRx = /import\s+(?:([A-Za-z0-9_]+)|\{([^}]+)\})\s+from\s+['"]([^'"]+)['"]/g;
  let match;
  while ((match = importRx.exec(text)) !== null) {
    const defaultName = match[1];
    const named = match[2] ? match[2].split(',').map(s => s.trim().split(/\s+as\s+/i)[0].trim()).filter(Boolean) : [];
    const source = match[3];
    const importedNames = [defaultName, ...named].filter(Boolean);
    for (const imported of importedNames) {
      if (components.includes(imported)) {
        const allowed = allowedByComponent[imported];
        if (allowed.length && !importSourceMatches(source, allowed)) {
          violations.push({
            type: 'wrong-component-import-source',
            file,
            line: lineNumber(text, match.index),
            component: imported,
            source,
            allowed
          });
        }
      }
    }
  }

  // function Button(...) or const Button = ... outside allowed source paths.
  for (const name of components) {
    const declRx = new RegExp(`(?:function\\s+${name}\\s*\\(|const\\s+${name}\\s*=|class\\s+${name}\\s+)`, 'g');
    let d;
    while ((d = declRx.exec(text)) !== null) {
      const allowed = allowedByComponent[name];
      const isAllowedFile = fileBelongsToAllowedSource(file, allowed);
      if (!isAllowedFile) {
        violations.push({ type: 'duplicate-component-declaration', file, line: lineNumber(text, d.index), component: name, allowed });
      }
    }
  }

  // Native primitives when DS has equivalents. In strict DS mode, these are violations outside DS source files.
  const primitiveMap = {
    Button: /<button\b/gi,
    Input: /<input\b/gi,
    TextArea: /<textarea\b/gi,
    Select: /<select\b/gi,
    Dialog: /<dialog\b/gi,
    Card: /className=['"][^'"]*\bcard\b/i
  };
  for (const [component, rx] of Object.entries(primitiveMap)) {
    if (!components.includes(component)) continue;
    let p;
    while ((p = rx.exec(text)) !== null) {
      const finding = { type: 'native-primitive-used-while-ds-component-exists', file, line: lineNumber(text, p.index), component, inDsSource };
      if (strictDs && !inDsSource) {
        violations.push({ ...finding, type: 'strict-ds-native-primitive-violation' });
      } else if (!inDsSource) {
        warnings.push(finding);
      }
    }
  }
}

const result = { manifestPath, root, strictDs, dsRoots, violations, warnings };
if (asJson) {
  console.log(JSON.stringify(result, null, 2));
} else {
  if (!violations.length && !warnings.length) console.log('No component contract findings.');
  for (const v of violations) console.log(`VIOLATION ${v.type} ${v.file}:${v.line} ${v.component || ''}`.trim(), JSON.stringify(v));
  for (const w of warnings) console.log(`WARNING ${w.type} ${w.file}:${w.line} ${w.component || ''}`.trim(), JSON.stringify(w));
  console.log(`\n${violations.length} violation(s), ${warnings.length} warning(s).`);
}

if (failOnViolation && violations.length > 0) process.exit(1);
if (failOnWarning && warnings.length > 0) process.exit(1);
