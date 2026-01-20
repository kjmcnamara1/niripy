"""
Niripy
===

Niripy is a python library which provides bindings for the `Niri <https://yalter.github.io/niri/>` wayland compositor.
"""

from icecream import ic

from niripy.instances import Instance

if __name__ == "__main__":
    niri = Instance()
    ic(niri.get_windows())
    ic(niri.get_focused_window())
    ic(niri.get_window_by_id(5))
    ic(niri.get_workspaces())
    ic(niri.get_focused_workspace())
    ic(niri.get_workspace_by_id(3))
    ic(niri.get_workspace_by_name("1"))
    ic(niri.get_outputs())
    ic(niri.get_focused_output())
    ic(niri.get_layers())
