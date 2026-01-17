"""
Niripy
===

Niripy is a python library which provides bindings for the `Niri <https://yalter.github.io/niri/>` wayland compositor.
"""

import json

from niripy.instances import Instance

if __name__ == "__main__":
    niri = Instance()
    request = {"Windows": None}
    print(niri.socket.send_command(json.dumps(request) + "\n"))
    print(niri.socket.send_command('{"FocusedWindow": null}\n'))
