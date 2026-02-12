# Niripy

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&style=for-the-badge)](#)
[![GitHub Release](https://img.shields.io/github/v/release/kjmcnamara1/niripy?style=for-the-badge&logo=github)](https://github.com/kjmcnamara1/niripy/releases/latest)
[![PyPI - Version](https://img.shields.io/pypi/v/niripy?style=for-the-badge&logo=pypi)](https://pypi.org/project/niripy)

<!-- [![AUR Version](https://img.shields.io/aur/version/python-niripy?style=for-the-badge&logo=archlinux)](https://aur.archlinux.org/packages/python-niripy) -->

Python bindings for the [Niri](https://yalter.github.io/niri) wayland compositor.

Credit to [hyprpy](https://github.com/ulinja/hyprpy) for providing inspiration and a great starting point.

> [!WARNING] Initial Development
> Niripy is still in very active and early stages of development.

## Quickstart

### Installation

#### Pip

```bash
pip install niripy
```

#### Uv

```bash
uv add niripy
```

<!-- #### Arch Linux -->

<!-- ```bash -->
<!-- yay -S python-niripy -->
<!-- ``` -->

### Examples

```py
from niripy import Instance

niri = Instance()

window = niri.get_active_window()
```
