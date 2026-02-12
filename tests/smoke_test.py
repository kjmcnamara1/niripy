"""Smoke tests to verify package is properly packaged."""


def test_niripy_imports():
    """Test that niripy module can be imported."""
    import niripy

    assert niripy is not None


def test_sockets_module_imports():
    """Test that niripy.sockets module can be imported."""
    from niripy import sockets

    assert sockets is not None


def test_socket_class_available():
    """Test that Socket class is available."""
    from niripy.sockets import Socket

    assert Socket is not None


def test_socket_error_available():
    """Test that SocketError exception is available."""
    from niripy.sockets import SocketError

    assert issubclass(SocketError, Exception)
