"""Tests for niripy.instances module."""

from unittest.mock import MagicMock, patch

import pytest

from niripy.instances import Instance, kebab_to_pascal
from niripy.models import (
    LayerSurface,
    Output,
    Window,
    Workspace,
)


class TestKebabToPascal:
    """Tests for kebab_to_pascal helper function."""

    def test_single_word(self):
        """Test conversion of single word."""
        assert kebab_to_pascal("version") == "Version"

    def test_kebab_case(self):
        """Test conversion of kebab-case string."""
        assert kebab_to_pascal("keyboard-layouts") == "KeyboardLayouts"

    def test_multiple_hyphens(self):
        """Test conversion of string with multiple hyphens."""
        assert kebab_to_pascal("focus-column-left") == "FocusColumnLeft"

    def test_empty_string(self):
        """Test conversion of empty string."""
        result = kebab_to_pascal("")
        assert isinstance(result, str)


class TestInstanceInit:
    """Tests for Instance initialization."""

    @patch("niripy.instances.Socket")
    def test_init_creates_socket(self, mock_socket_class):
        """Test that __init__ creates a Socket instance."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        # Mock the _request method to avoid actual socket communication
        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.version = "0.1.0"
            mock_request.return_value = mock_response

            instance = Instance()

            assert instance.socket is mock_socket
            mock_socket_class.assert_called_once()

    @patch("niripy.instances.Socket")
    def test_init_sets_version(self, mock_socket_class):
        """Test that __init__ sets version from _request."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.version = "0.2.0"
            mock_request.return_value = mock_response

            instance = Instance()

            assert instance.version == "0.2.0"
            mock_request.assert_called_once_with("version")

    @patch("niripy.instances.Socket")
    def test_init_version_fallback(self, mock_socket_class):
        """Test that version defaults to 'unknown' if request returns None."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.version = None
            mock_request.return_value = mock_response

            instance = Instance()

            assert instance.version == "unknown"


class TestInstanceRepr:
    """Tests for Instance __repr__ method."""

    @patch("niripy.instances.Socket")
    def test_repr_format(self, mock_socket_class):
        """Test __repr__ returns correct format."""
        mock_socket = MagicMock()
        mock_socket.path = "/tmp/niri-socket"
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.version = "0.1.0"
            mock_request.return_value = mock_response

            instance = Instance()
            repr_str = repr(instance)

            assert repr_str.startswith("<Instance(socket=")
            assert "/tmp/niri-socket" in repr_str
            assert repr_str.endswith(")>")


class TestInstanceRequest:
    """Tests for Instance._request method."""

    @patch("niripy.instances.Socket")
    def test_request_converts_command_to_pascal(self, mock_socket_class):
        """Test that _request converts kebab-case command to PascalCase."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(
            return_value='{"Reply":{"Ok":{"Version":"0.1.0"}}}'
        )
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            mock_reply = MagicMock()
            mock_response = MagicMock()
            mock_reply.unwrap.return_value = mock_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            mock_socket.send_command.reset_mock()  # Reset to clear init call
            instance._request("version")

            # Verify socket.send_command was called with PascalCase
            mock_socket.send_command.assert_called_once()

    @patch("niripy.instances.Socket")
    def test_request_with_context(self, mock_socket_class):
        """Test that _request passes instance context to model_validate_json."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(return_value="{}")
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            mock_reply = MagicMock()
            mock_response = MagicMock()
            mock_reply.unwrap.return_value = mock_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            instance._request("windows")

            # Verify context was passed
            call_args = mock_validate.call_args
            assert call_args[1]["context"]["instance"] is instance

    @patch("niripy.instances.Socket")
    def test_request_returns_unwrapped_response(self, mock_socket_class):
        """Test that _request returns the unwrapped response."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(return_value="{}")
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            expected_response = MagicMock()
            mock_reply = MagicMock()
            mock_reply.unwrap.return_value = expected_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            result = instance._request("windows")

            assert result is expected_response


class TestInstanceAction:
    """Tests for Instance.action method."""

    @patch("niripy.instances.Socket")
    def test_action_converts_to_pascal(self, mock_socket_class):
        """Test that action converts kebab-case to PascalCase."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(return_value="{}")
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            mock_reply = MagicMock()
            mock_response = MagicMock()
            mock_response.handled = True
            mock_reply.unwrap.return_value = mock_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            instance.action("close-window")

            # Verify the command structure
            call_args = mock_socket.send_command.call_args[0][0]
            assert "Action" in call_args
            assert "CloseWindow" in call_args["Action"]

    @patch("niripy.instances.Socket")
    def test_action_with_kwargs(self, mock_socket_class):
        """Test that action passes kwargs to the request."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(return_value="{}")
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            mock_reply = MagicMock()
            mock_response = MagicMock()
            mock_response.handled = True
            mock_reply.unwrap.return_value = mock_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            instance.action("spawn", command="alacritty")

            # Verify kwargs were included
            call_args = mock_socket.send_command.call_args[0][0]
            assert call_args["Action"]["Spawn"]["command"] == "alacritty"

    @patch("niripy.instances.Socket")
    def test_action_returns_handled_status(self, mock_socket_class):
        """Test that action returns handled status."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(return_value="{}")
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            mock_reply = MagicMock()
            mock_response = MagicMock()
            mock_response.handled = True
            mock_reply.unwrap.return_value = mock_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            result = instance.action("quit")

            assert result is True

    @patch("niripy.instances.Socket")
    def test_action_returns_false_when_not_handled(self, mock_socket_class):
        """Test that action returns False when not handled."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(return_value="{}")
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            mock_reply = MagicMock()
            mock_response = MagicMock()
            mock_response.handled = False
            mock_reply.unwrap.return_value = mock_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            result = instance.action("quit")

            assert result is False

    @patch("niripy.instances.Socket")
    def test_action_returns_false_when_handled_is_none(self, mock_socket_class):
        """Test that action returns False when handled is None."""
        mock_socket = MagicMock()
        mock_socket.send_command = MagicMock(return_value="{}")
        mock_socket_class.return_value = mock_socket

        with patch("niripy.instances.Reply.model_validate_json") as mock_validate:
            mock_reply = MagicMock()
            mock_response = MagicMock()
            mock_response.handled = None
            mock_reply.unwrap.return_value = mock_response
            mock_validate.return_value = mock_reply

            instance = Instance()
            result = instance.action("quit")

            assert result is False


class TestInstanceGetWindows:
    """Tests for Instance.get_windows method."""

    @patch("niripy.instances.Socket")
    def test_get_windows_returns_list(self, mock_socket_class):
        """Test that get_windows returns a list of windows."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        window1 = MagicMock(spec=Window)
        window2 = MagicMock(spec=Window)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.windows = [window1, window2]
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_windows()

            assert result == [window1, window2]
            mock_request.assert_called_with("windows")

    @patch("niripy.instances.Socket")
    def test_get_windows_returns_empty_list_when_none(self, mock_socket_class):
        """Test that get_windows returns empty list when response.windows is None."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.windows = None
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_windows()

            assert result == []


class TestInstanceGetFocusedWindow:
    """Tests for Instance.get_focused_window method."""

    @patch("niripy.instances.Socket")
    def test_get_focused_window_returns_window(self, mock_socket_class):
        """Test that get_focused_window returns the focused window."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        focused_window = MagicMock(spec=Window)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.focused_window = focused_window
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_focused_window()

            assert result is focused_window

    @patch("niripy.instances.Socket")
    def test_get_focused_window_raises_when_none(self, mock_socket_class):
        """Test that get_focused_window raises ValueError when no focused window."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.focused_window = None
            mock_request.return_value = mock_response

            instance = Instance()

            with pytest.raises(ValueError, match="Unable to retrieve focused window"):
                instance.get_focused_window()


class TestInstanceGetWindowById:
    """Tests for Instance.get_window_by_id method."""

    def test_get_window_by_id_returns_matching_window(self):
        """Test that get_window_by_id returns window with matching id."""
        window1 = MagicMock(spec=Window)
        window1.id = 1
        window2 = MagicMock(spec=Window)
        window2.id = 2

        instance = MagicMock(spec=Instance)
        instance.get_windows.return_value = [window1, window2]

        result = Instance.get_window_by_id(instance, 2)

        assert result is window2

    def test_get_window_by_id_returns_none_when_not_found(self):
        """Test that get_window_by_id returns None when id not found."""
        window1 = MagicMock(spec=Window)
        window1.id = 1

        instance = MagicMock(spec=Instance)
        instance.get_windows.return_value = [window1]

        result = Instance.get_window_by_id(instance, 999)

        assert result is None


class TestInstanceGetWorkspaces:
    """Tests for Instance.get_workspaces method."""

    @patch("niripy.instances.Socket")
    def test_get_workspaces_returns_list(self, mock_socket_class):
        """Test that get_workspaces returns a list of workspaces."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        workspace1 = MagicMock(spec=Workspace)
        workspace2 = MagicMock(spec=Workspace)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.workspaces = [workspace1, workspace2]
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_workspaces()

            assert result == [workspace1, workspace2]
            mock_request.assert_called_with("workspaces")

    @patch("niripy.instances.Socket")
    def test_get_workspaces_returns_empty_list_when_none(self, mock_socket_class):
        """Test that get_workspaces returns empty list when response.workspaces is None."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.workspaces = None
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_workspaces()

            assert result == []


class TestInstanceGetFocusedWorkspace:
    """Tests for Instance.get_focused_workspace method."""

    def test_get_focused_workspace_returns_focused(self):
        """Test that get_focused_workspace returns the focused workspace."""
        workspace1 = MagicMock(spec=Workspace)
        workspace1.is_focused = False
        workspace2 = MagicMock(spec=Workspace)
        workspace2.is_focused = True

        instance = MagicMock(spec=Instance)
        instance.get_workspaces.return_value = [workspace1, workspace2]
        result = Instance.get_focused_workspace(instance)

        assert result is workspace2

    def test_get_focused_workspace_raises_when_none(self):
        """Test that get_focused_workspace raises ValueError when no focused workspace."""
        workspace = MagicMock(spec=Workspace)
        workspace.is_focused = False

        instance = MagicMock(spec=Instance)
        instance.get_workspaces.return_value = [workspace]

        with pytest.raises(ValueError, match="Unable to retrieve focused workspace"):
            Instance.get_focused_workspace(instance)


class TestInstanceGetWorkspaceById:
    """Tests for Instance.get_workspace_by_id method."""

    def test_get_workspace_by_id_returns_matching_workspace(self):
        """Test that get_workspace_by_id returns workspace with matching id."""
        workspace1 = MagicMock(spec=Workspace)
        workspace1.id = 1
        workspace2 = MagicMock(spec=Workspace)
        workspace2.id = 2

        instance = MagicMock(spec=Instance)
        instance.get_workspaces.return_value = [workspace1, workspace2]

        result = Instance.get_workspace_by_id(instance, 2)

        assert result is workspace2

    def test_get_workspace_by_id_returns_none_when_not_found(self):
        """Test that get_workspace_by_id returns None when id not found."""
        workspace = MagicMock(spec=Workspace)
        workspace.id = 1

        instance = MagicMock(spec=Instance)
        instance.get_workspaces.return_value = [workspace]

        result = Instance.get_workspace_by_id(instance, 999)

        assert result is None


class TestInstanceGetWorkspaceByName:
    """Tests for Instance.get_workspace_by_name method."""

    def test_get_workspace_by_name_returns_matching_workspace(self):
        """Test that get_workspace_by_name returns workspace with matching name."""
        workspace1 = MagicMock(spec=Workspace)
        workspace1.name = "workspace-1"
        workspace2 = MagicMock(spec=Workspace)
        workspace2.name = "workspace-2"

        instance = MagicMock(spec=Instance)
        instance.get_workspaces.return_value = [workspace1, workspace2]

        result = Instance.get_workspace_by_name(instance, "workspace-2")

        assert result is workspace2

    def test_get_workspace_by_name_returns_none_when_not_found(self):
        """Test that get_workspace_by_name returns None when name not found."""
        workspace = MagicMock(spec=Workspace)
        workspace.name = "workspace-1"

        instance = MagicMock(spec=Instance)
        instance.get_workspaces.return_value = [workspace]

        result = Instance.get_workspace_by_name(instance, "non-existent")

        assert result is None


class TestInstanceGetOutputs:
    """Tests for Instance.get_outputs method."""

    @patch("niripy.instances.Socket")
    def test_get_outputs_returns_list(self, mock_socket_class):
        """Test that get_outputs returns a list of outputs."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        output1 = MagicMock(spec=Output)
        output2 = MagicMock(spec=Output)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.outputs = {"HDMI-1": output1, "DP-1": output2}
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_outputs()

            assert len(result) == 2
            assert output1 in result
            assert output2 in result
            mock_request.assert_called_with("outputs")

    @patch("niripy.instances.Socket")
    def test_get_outputs_returns_empty_list_when_none(self, mock_socket_class):
        """Test that get_outputs returns empty list when response.outputs is None."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.outputs = None
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_outputs()

            assert result == []


class TestInstanceGetFocusedOutput:
    """Tests for Instance.get_focused_output method."""

    @patch("niripy.instances.Socket")
    def test_get_focused_output_returns_output(self, mock_socket_class):
        """Test that get_focused_output returns the focused output."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        focused_output = MagicMock(spec=Output)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.focused_output = focused_output
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_focused_output()

            assert result is focused_output

    @patch("niripy.instances.Socket")
    def test_get_focused_output_raises_when_none(self, mock_socket_class):
        """Test that get_focused_output raises ValueError when no focused output."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.focused_output = None
            mock_request.return_value = mock_response

            instance = Instance()

            with pytest.raises(ValueError, match="Unable to retrieve focused output"):
                instance.get_focused_output()


class TestInstanceGetOutputByName:
    """Tests for Instance.get_output_by_name method."""

    @patch("niripy.instances.Socket")
    def test_get_output_by_name_returns_matching_output(self, mock_socket_class):
        """Test that get_output_by_name returns output with matching name."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        output1 = MagicMock(spec=Output)
        output2 = MagicMock(spec=Output)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.outputs = {"HDMI-1": output1, "DP-1": output2}
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_output_by_name("DP-1")

            assert result is output2

    @patch("niripy.instances.Socket")
    def test_get_output_by_name_returns_none_when_not_found(self, mock_socket_class):
        """Test that get_output_by_name returns None when name not found."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        output = MagicMock(spec=Output)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.outputs = {"HDMI-1": output}
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_output_by_name("non-existent")

            assert result is None

    @patch("niripy.instances.Socket")
    def test_get_output_by_name_returns_none_when_outputs_none(self, mock_socket_class):
        """Test that get_output_by_name returns None when outputs is None."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.outputs = None
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_output_by_name("HDMI-1")

            assert result is None


class TestInstanceGetLayers:
    """Tests for Instance.get_layers method."""

    @patch("niripy.instances.Socket")
    def test_get_layers_returns_list(self, mock_socket_class):
        """Test that get_layers returns a list of layer surfaces."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        layer1 = MagicMock(spec=LayerSurface)
        layer2 = MagicMock(spec=LayerSurface)

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.layers = [layer1, layer2]
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_layers()

            assert result == [layer1, layer2]
            mock_request.assert_called_with("layers")

    @patch("niripy.instances.Socket")
    def test_get_layers_returns_empty_list_when_none(self, mock_socket_class):
        """Test that get_layers returns empty list when response.layers is None."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        with patch.object(Instance, "_request") as mock_request:
            mock_response = MagicMock()
            mock_response.layers = None
            mock_request.return_value = mock_response

            instance = Instance()
            result = instance.get_layers()

            assert result == []
