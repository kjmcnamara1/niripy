# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Change public API:
  - [ ] Instance -> NiriInstance?
  - [ ] Socket -> \_NiriSocket(ABC/Protocol)?
    - [ ] CommandSocket
    - [ ] EventSocket
  - [ ] RequestCmd -> StrEnum?
  - [ ] ActionCmd -> StrEnum?

- Document RequestCmd and ActionCmd

- Automate version bumping?
  - [Commitizen](https://commitizen-tools.github.io/commitizen/)

- Second socket for listening to event-stream
- Instance.watch method for events
- Add tests for event-stream

- Audit unit tests
- Second look at sockets

## [0.2.8] -

### Added

- Add NiriPy version to docs/index.md
- [markdown-pycon](https://pawamoy.github.io/markdown-pycon/) for mkdocs

### Removed

- ModelWithInstance from public API
- kebab_to_pascal from public API

### Changed

- LayerSurface.output -> LayerSurface.get_output()
- Output.workspaces -> Output.get_workspaces()
- Output.layers -> Output.get_layers()
- Output.windows -> Output.get_windows()
- Window.workspace -> Window.get_workspace()
- Workspace.output -> Workspace.get_output()
- Workspace.active_window -> Workspace.get_active_window()
- Workspace.windows -> Workspace.get_windows()

- Use ty instead of pyright for type checking

## [0.2.7] - 2026-02-23

### Added

- Permissions to calling cicd workflow for release, pypi, and docs

## [0.2.6] - 2026-02-23

### Added

- AUR package
- Github workflow for publishing to AUR
- flake.nix
- Documentation site <https://kjmcnamara1.github.io/niripy>
- Github workflow for deploying documentation site

### Changed

- AUR shield and install in README.md

### Removed

- instances.T and imports TypeVar and ModelWithInstance

## [0.2.5] - 2026-02-11

### Removed

- dev imports from `__init__.py`

## [0.2.4] - 2026-02-11

### Added

- Smoke test to verify package is properly packaged

## [0.2.3] - 2026-02-11

### Fixed

- **$NIRI_SOCKET** is no longer required as long as _path_to_socket_ is provided
- Added 'shell' for composite github action
- Paths to composite github action from workflows

## [0.2.2] - 2026-02-11

### Added

- Pyright for type checking
- Github workflows for code quality and publishing

### Changed

- Updated shields in README.md

## [0.2.1] 2026-02-11

### Added

- Initial README
- CHANGELOG
- Unit tests
- Vermin to test group for static python version detection

### Changed

- Pinned Python version 3.12 -> 3.14
- Minimum required python version still 3.12

### Removed

- unused imports

### Fixed

- Output.workspaces not producing list of workspaces
- Suppress pyright typechecking errors

## [0.2.0] 2026-01-24

### Added

## [0.1.0] 2026-01-16

### Added

- Instance class
