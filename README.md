# Niripy

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&style=for-the-badge)](#)
[![GitHub Release](https://img.shields.io/github/v/release/kjmcnamara1/niripy?style=for-the-badge&logo=github)](https://github.com/kjmcnamara1/niripy/releases/latest)
[![PyPI - Version](https://img.shields.io/pypi/v/niripy?style=for-the-badge&logo=pypi)](https://pypi.org/project/niripy)
[![AUR Version](https://img.shields.io/aur/version/python-niripy?style=for-the-badge&logo=archlinux)](https://aur.archlinux.org/packages/python-niripy)

Python bindings for the [Niri](https://yalter.github.io/niri) wayland compositor.

## Quickstart

### Installation

#### [Python Package Index](https://pypi.org/)

Install with any of the following depending on your python package manager:

```bash
pip install niripy
poetry add niripy
uv add niripy
```

#### Arch Linux

The package is also available on the [AUR](https://aur.archlinux.org):

```bash
yay -S python-niripy
```

### Examples

```py
from niripy import Instance

niri = Instance()

window = niri.get_active_window()
```

## Development

> [!WARNING]
> **Initial Development**
> Niripy is still in very active and early stages of development.

Please file an issue if you find any bugs or have a feature request.

Credit to [hyprpy](https://github.com/ulinja/hyprpy) for providing inspiration and a great starting point.

### Roadmap

- [x] Add AUR package
- [x] Add flake.nix
- [ ] Generate documentation with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [ ] Second socket for listening to event-stream
- [ ] Instance.watch method for events

### Nix

This repository provides a nix flake for development.

```sh
nix develop
python --version
python -c "import pydantic; print(pydantic.__version__)"
python -c "import niripy"
```
