import json
import os
import select
import socket
from pathlib import Path
from typing import Any, override


class SocketError(Exception):
    """Raised when a socket operation fails."""

    pass


class Socket:
    path: Path
    _socket: socket.socket | None

    def __init__(self, path_to_socket: str = ""):
        niri_socket: str = os.getenv("NIRI_SOCKET", "")
        if not niri_socket:
            raise RuntimeError(
                "$NIRI_SOCKET is not defined. Are you running inside a niri session?"
            )

        self.path = Path(path_to_socket or niri_socket)

        if not self.path.is_socket():
            raise FileNotFoundError(f"No socket found at {self.path!r}.")
        self._socket = None

    @override
    def __repr__(self) -> str:
        return f"<Socket(path={str(self.path)!r})>"

    def connect(self, timeout: float | None = 1.0):
        if self._socket:
            raise SocketError("Connect to socket failed: Socket is already connected.")

        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self._socket.connect(str(self.path))
        self._socket.setblocking(False)

    def close(self):
        if not self._socket:
            raise SocketError("Close socket failed: Socket is not connected.")

        self._socket.close()
        self._socket = None

    def send(self, data: str):
        if not self._socket:
            raise SocketError("Send data to socket failed: Socket is not connected.")

        self._socket.sendall(data.encode("utf-8"))

    def wait(self, timeout: float | None = None):
        if not self._socket:
            raise SocketError(
                "Wait for data on socket failed: Socket is not connected."
            )

        ready, _, _ = select.select([self._socket], [], [], timeout)
        if not ready:
            raise SocketError("Wait for data on socket failed after {timeout} seconds.")

    def read(self) -> str:
        if not self._socket:
            raise SocketError("Read data from socket failed: Socket is not connected.")

        data = bytearray()
        while True:
            try:
                data_chunk = self._socket.recv(4096)
                if data_chunk:
                    data += data_chunk
                else:
                    break
            except BlockingIOError as e:
                if e.errno == 11:
                    break
                else:
                    raise SocketError("Read data from socket failed.") from e

        return data.decode("utf-8")

    def send_command(self, message: dict[str, Any] | str) -> str:
        """
        Send a command message and retrieve the response.

        Establishes a connection, sends the provided message, waits for processing,
        reads the response, and closes the connection.

        Args:
            message (str): The command message to send. (JSON formatted)

        Returns:
            str: The response received from the remote endpoint. (JSON formatted)
        """
        self.connect()
        self.send(json.dumps(message) + "\n")
        self.wait(5)
        response = self.read()
        self.close()

        return response
