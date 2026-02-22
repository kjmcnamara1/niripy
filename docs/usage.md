# Usage

Quick start and examples.

## Install

Install from [PyPI](https://pypi.org/project/niripy/) or the [AUR](https://aur.archlinux.org/packages/python-niripy):

```sh
# PyPI
pip install niripy
poetry add niripy
uv add niripy

# AUR
yay -S python-niripy
paru -S python-niripy
```

Or use Nix with the provided flake:

```sh
nix develop github:kjmcnamara1/niripy
```

## Examples

[Instance][niripy.Instance] is the main class for interacting with Niri. It
attaches to the Niri socket and provides methods for querying and controlling
Niri.

The models returned (e.g. [Windows][niripy.models.Window],
[Outputs][niripy.models.Output], [Workspaces][niripy.models.Workspace]) are all
pydantic models!

```py linenums="1"
from niripy.instances import Instance

niri = Instance()

print(niri.version)

for window in niri.get_windows():
    print(window.title)
    print(window.model_dump_json(indent=2))
```
