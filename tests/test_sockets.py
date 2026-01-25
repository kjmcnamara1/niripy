"""Tests for niripy.sockets module."""

import json
import os
import socket
from unittest.mock import MagicMock, patch

import pytest

from niripy.sockets import Socket, SocketError


@pytest.fixture
def socket_path(tmp_path):
    """Create a temporary Unix socket for testing."""
    socket_file = tmp_path / "test.sock"
    # Create a real socket file
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(str(socket_file))
    sock.listen(1)
    yield socket_file
    sock.close()
    if socket_file.exists():
        socket_file.unlink()


@pytest.fixture
def mock_env_socket(socket_path):
    """Mock NIRI_SOCKET environment variable."""
    with patch.dict(os.environ, {"NIRI_SOCKET": str(socket_path)}):
        yield socket_path


class TestSocketInit:
    """Tests for Socket initialization."""

    def test_init_with_env_var(self, mock_env_socket):
        """Test Socket initialization using NIRI_SOCKET env var."""
        socket_obj = Socket()
        assert socket_obj.path == mock_env_socket
        assert socket_obj._socket is None

    def test_init_with_explicit_path(self, socket_path):
        """Test Socket initialization with explicit path."""
        socket_obj = Socket(str(socket_path))
        assert socket_obj.path == socket_path
        assert socket_obj._socket is None

    def test_init_missing_env_var(self):
        """Test Socket initialization fails when NIRI_SOCKET is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(RuntimeError, match="NIRI_SOCKET is not defined"):
                Socket()

    def test_init_invalid_socket_path(self):
        """Test Socket initialization fails with non-existent path."""
        with patch.dict(os.environ, {"NIRI_SOCKET": "/nonexistent/path.sock"}):
            with pytest.raises(FileNotFoundError, match="No socket found at"):
                Socket()

    def test_init_explicit_path_takes_precedence(self, socket_path):
        """Test that explicit path takes precedence over env var."""
        with patch.dict(os.environ, {"NIRI_SOCKET": "/some/other/path.sock"}):
            socket_obj = Socket(str(socket_path))
            assert socket_obj.path == socket_path


class TestSocketRepr:
    """Tests for Socket string representation."""

    def test_repr(self, mock_env_socket):
        """Test Socket __repr__ method."""
        socket_obj = Socket()
        assert "Socket" in repr(socket_obj)
        assert str(mock_env_socket) in repr(socket_obj)


class TestSocketConnect:
    """Tests for Socket connect method."""

    def test_connect_sets_socket(self, mock_env_socket):
        """Test that connect creates and sets _socket attribute."""
        with patch("niripy.sockets.socket.socket") as mock_socket_class:
            mock_socket = MagicMock()
            mock_socket_class.return_value = mock_socket

            socket_obj = Socket()
            socket_obj.connect()

            assert socket_obj._socket is not None
            mock_socket.connect.assert_called_once()

    def test_connect_already_connected(self, mock_env_socket):
        """Test connect raises error when already connected."""
        socket_obj = Socket()
        socket_obj._socket = MagicMock()  # Simulate already connected

        with pytest.raises(SocketError, match="already connected"):
            socket_obj.connect()

    def test_connect_with_timeout(self, mock_env_socket):
        """Test connect with custom timeout."""
        with patch("niripy.sockets.socket.socket") as mock_socket_class:
            mock_socket = MagicMock()
            mock_socket_class.return_value = mock_socket

            socket_obj = Socket()
            socket_obj.connect(timeout=2.5)

            mock_socket.settimeout.assert_called_once_with(2.5)

    def test_connect_sets_non_blocking(self, mock_env_socket):
        """Test connect sets socket to non-blocking mode."""
        with patch("niripy.sockets.socket.socket") as mock_socket_class:
            mock_socket = MagicMock()
            mock_socket_class.return_value = mock_socket

            socket_obj = Socket()
            socket_obj.connect()

            mock_socket.setblocking.assert_called_once_with(False)


class TestSocketClose:
    """Tests for Socket close method."""

    def test_close_connected_socket(self, mock_env_socket):
        """Test closing a connected socket."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        socket_obj.close()

        mock_socket.close.assert_called_once()
        assert socket_obj._socket is None

    def test_close_disconnected_socket(self, mock_env_socket):
        """Test close raises error when not connected."""
        socket_obj = Socket()
        socket_obj._socket = None

        with pytest.raises(SocketError, match="not connected"):
            socket_obj.close()


class TestSocketSend:
    """Tests for Socket send method."""

    def test_send_connected_socket(self, mock_env_socket):
        """Test sending data through connected socket."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        test_data = "test message"
        socket_obj.send(test_data)

        mock_socket.sendall.assert_called_once_with(test_data.encode("utf-8"))

    def test_send_disconnected_socket(self, mock_env_socket):
        """Test send raises error when not connected."""
        socket_obj = Socket()
        socket_obj._socket = None

        with pytest.raises(SocketError, match="not connected"):
            socket_obj.send("test")

    def test_send_encodes_utf8(self, mock_env_socket):
        """Test that send properly encodes to UTF-8."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        test_data = "café"
        socket_obj.send(test_data)

        mock_socket.sendall.assert_called_once_with(test_data.encode("utf-8"))


class TestSocketWait:
    """Tests for Socket wait method."""

    def test_wait_data_available(self, mock_env_socket):
        """Test wait returns when data is available."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        with patch("niripy.sockets.select.select") as mock_select:
            mock_select.return_value = ([mock_socket], [], [])
            socket_obj.wait()
            mock_select.assert_called_once()

    def test_wait_timeout(self, mock_env_socket):
        """Test wait raises error on timeout."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        with patch("niripy.sockets.select.select") as mock_select:
            mock_select.return_value = ([], [], [])
            with pytest.raises(SocketError, match="after"):
                socket_obj.wait(timeout=1.0)

    def test_wait_disconnected_socket(self, mock_env_socket):
        """Test wait raises error when not connected."""
        socket_obj = Socket()
        socket_obj._socket = None

        with pytest.raises(SocketError, match="not connected"):
            socket_obj.wait()

    def test_wait_with_custom_timeout(self, mock_env_socket):
        """Test wait with custom timeout value."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        with patch("niripy.sockets.select.select") as mock_select:
            mock_select.return_value = ([mock_socket], [], [])
            socket_obj.wait(timeout=5.0)

            # Verify timeout was passed to select
            call_args = mock_select.call_args
            assert call_args[0][3] == 5.0


class TestSocketRead:
    """Tests for Socket read method."""

    def test_read_single_chunk(self, mock_env_socket):
        """Test reading data in a single chunk."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        test_data = "test response"
        mock_socket.recv.side_effect = [test_data.encode("utf-8"), b""]

        result = socket_obj.read()

        assert result == test_data

    def test_read_multiple_chunks(self, mock_env_socket):
        """Test reading data in multiple chunks."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        chunk1 = b"part1"
        chunk2 = b"part2"
        mock_socket.recv.side_effect = [chunk1, chunk2, b""]

        result = socket_obj.read()

        assert result == "part1part2"

    def test_read_blocking_io_error(self, mock_env_socket):
        """Test read handles BlockingIOError with errno 11."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        test_data = b"test"
        error = BlockingIOError()
        error.errno = 11
        mock_socket.recv.side_effect = [test_data, error]

        result = socket_obj.read()

        assert result == "test"

    def test_read_blocking_io_error_other_errno(self, mock_env_socket):
        """Test read raises SocketError on BlockingIOError with other errno."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        error = BlockingIOError()
        error.errno = 999
        mock_socket.recv.side_effect = error

        with pytest.raises(SocketError, match="Read data from socket failed"):
            socket_obj.read()

    def test_read_disconnected_socket(self, mock_env_socket):
        """Test read raises error when not connected."""
        socket_obj = Socket()
        socket_obj._socket = None

        with pytest.raises(SocketError, match="not connected"):
            socket_obj.read()

    def test_read_empty_response(self, mock_env_socket):
        """Test reading empty response."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        mock_socket.recv.return_value = b""

        result = socket_obj.read()

        assert result == ""

    def test_read_utf8_decoding(self, mock_env_socket):
        """Test read properly decodes UTF-8."""
        socket_obj = Socket()
        mock_socket = MagicMock()
        socket_obj._socket = mock_socket

        test_data = "café".encode("utf-8")
        mock_socket.recv.side_effect = [test_data, b""]

        result = socket_obj.read()

        assert result == "café"


class TestSocketSendCommand:
    """Tests for Socket send_command method."""

    def test_send_command_dict(self, mock_env_socket):
        """Test send_command with dictionary input."""
        socket_obj = Socket()

        test_dict = {"Action": {"FocusOutput": {}}}
        expected_response = '{"result": "success"}'

        with (
            patch.object(socket_obj, "connect") as mock_connect,
            patch.object(socket_obj, "send") as mock_send,
            patch.object(socket_obj, "wait") as mock_wait,
            patch.object(socket_obj, "read") as mock_read,
            patch.object(socket_obj, "close") as mock_close,
        ):
            mock_read.return_value = expected_response

            result = socket_obj.send_command(test_dict)

            assert result == expected_response
            mock_connect.assert_called_once()
            mock_send.assert_called_once()
            mock_wait.assert_called_once_with(5)
            mock_read.assert_called_once()
            mock_close.assert_called_once()

    def test_send_command_string(self, mock_env_socket):
        """Test send_command with string input."""
        socket_obj = Socket()

        test_str = '{"Action": {"FocusOutput": {}}}'
        expected_response = '{"result": "success"}'

        with (
            patch.object(socket_obj, "connect") as mock_connect,
            patch.object(socket_obj, "send") as mock_send,
            patch.object(socket_obj, "wait") as mock_wait,
            patch.object(socket_obj, "read") as mock_read,
            patch.object(socket_obj, "close") as mock_close,
        ):
            mock_read.return_value = expected_response

            result = socket_obj.send_command(test_str)

            assert result == expected_response

    def test_send_command_jsonifies_dict(self, mock_env_socket):
        """Test send_command properly JSON-encodes dict and adds newline."""
        socket_obj = Socket()

        test_dict = {"Test": "value"}

        with (
            patch.object(socket_obj, "connect"),
            patch.object(socket_obj, "send") as mock_send,
            patch.object(socket_obj, "wait"),
            patch.object(socket_obj, "read", return_value=""),
            patch.object(socket_obj, "close"),
        ):
            socket_obj.send_command(test_dict)

            # Verify send was called with JSON + newline
            call_args = mock_send.call_args[0][0]
            assert call_args == json.dumps(test_dict) + "\n"

    def test_send_command_closes_on_success(self, mock_env_socket):
        """Test send_command closes connection even on success."""
        socket_obj = Socket()

        with (
            patch.object(socket_obj, "connect"),
            patch.object(socket_obj, "send"),
            patch.object(socket_obj, "wait"),
            patch.object(socket_obj, "read", return_value='{"status": "ok"}'),
            patch.object(socket_obj, "close") as mock_close,
        ):
            socket_obj.send_command({"test": "data"})

            mock_close.assert_called_once()

    def test_send_command_full_workflow(self, mock_env_socket):
        """Test complete send_command workflow."""
        socket_obj = Socket()

        command = {"Action": {"Version": {}}}
        response = '{"Response": {"Version": {"version": "0.1.0"}}}'

        with (
            patch.object(socket_obj, "connect") as mock_connect,
            patch.object(socket_obj, "send") as mock_send,
            patch.object(socket_obj, "wait") as mock_wait,
            patch.object(socket_obj, "read") as mock_read,
            patch.object(socket_obj, "close") as mock_close,
        ):
            mock_read.return_value = response

            result = socket_obj.send_command(command)

            # Verify call sequence
            assert mock_connect.call_count == 1
            assert mock_send.call_count == 1
            assert mock_wait.call_count == 1
            assert mock_read.call_count == 1
            assert mock_close.call_count == 1
            assert result == response


class TestSocketIntegration:
    """Integration tests for Socket class."""

    def test_socket_lifecycle(self, mock_env_socket):
        """Test complete socket lifecycle: connect, send, read, close."""
        socket_obj = Socket()

        with (
            patch.object(socket_obj, "connect") as mock_connect,
            patch.object(socket_obj, "send") as mock_send,
            patch.object(socket_obj, "read", return_value="response"),
            patch.object(socket_obj, "close") as mock_close,
        ):
            socket_obj.connect()
            socket_obj.send("test")
            response = socket_obj.read()
            socket_obj.close()

            assert response == "response"
            mock_connect.assert_called_once()
            mock_send.assert_called_once()
            mock_close.assert_called_once()

    def test_socket_cannot_double_connect(self, mock_env_socket):
        """Test socket cannot be connected twice without closing."""
        socket_obj = Socket()
        socket_obj._socket = MagicMock()

        with pytest.raises(SocketError):
            socket_obj.connect()
