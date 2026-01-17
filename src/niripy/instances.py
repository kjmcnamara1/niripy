from niripy.sockets import Socket


class Instance:
    def __init__(self):
        self.socket: Socket = Socket()
