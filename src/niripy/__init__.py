"""
Niripy
===

Niripy is a python library which provides bindings for the `Niri <https://yalter.github.io/niri/>` wayland compositor.
"""

from icecream import ic

from niripy.instances import Instance

if __name__ == "__main__":
    niri = Instance()

    v = niri._request("version")
    ic(v)
    ic(v.unwrap())
