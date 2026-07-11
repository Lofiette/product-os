# Platform Support

The migration assistant uses Python `pathlib`, atomic replacement and Git commands without shell-specific scripts.

Supported targets for CI:

- Linux;
- macOS;
- Windows;
- WSL.

## WSL

Both Linux-home and mounted Windows repositories are supported. The platform checker warns when a repository is under `/mnt/` because filesystem behavior and performance may differ.

## Windows

Use a sufficiently recent Python and Git. Long project paths may require the OS/Git long-path configuration. The assistant does not rely on symlinks.

## Local state

Plans and backups default to the user-level CPT home, outside the product repository. Set `CPT_HOME` or `--backup-dir` to relocate them.
