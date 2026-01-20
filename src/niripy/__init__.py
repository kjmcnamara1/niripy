"""
Niripy
===

Niripy is a python library which provides bindings for the `Niri <https://yalter.github.io/niri/>` wayland compositor.
"""

from icecream import ic

from niripy.instances import Instance

if __name__ == "__main__":
    niri = Instance()

    o = niri.get_focused_output()
    ic(o)
    ic(niri.get_output_by_name(o.name))

    ws = niri.get_focused_workspace()
    ic(ws)
    ic(ws.model_dump())
    ic(ws.active_window)
    ic(ws.output)
    ic(ws.windows)
