"""
Niripy
===

Niripy is a python library which provides bindings for the `Niri <https://yalter.github.io/niri/>` wayland compositor.
"""

from icecream import ic

from niripy.instances import Instance

if __name__ == "__main__":
    niri = Instance()

    # ic(niri.socket.send_command('{"Version":null}\n'))
    # ic(niri.socket.send_command('"Version"\n'))
    # ic(niri.socket.send_command('{"Action":{"FocusWindow":{"id":2}}}\n'))

    ic(niri._request("version"))
    # ic(niri._request("focused-window"))
    ic(niri._action("focus-window", id=2))
