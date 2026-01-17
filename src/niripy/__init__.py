"""
Niripy
===

Niripy is a python library which provides bindings for the `Niri <https://yalter.github.io/niri/>` wayland compositor.
"""

from niripy.instances import Instance

if __name__ == "__main__":
    niri = Instance()
    niri.socket.connect()
    print(niri)
    print(niri.socket)
    print(niri.socket._socket)
    print(niri.socket._path_to_socket)
