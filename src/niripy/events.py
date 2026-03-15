import json

from typing import Optional, Any

from niripy.models import (
    Workspace,
    Window,
    WindowLayout,
    KeyboardLayouts,
    Cast,
    Timestamp,
)
from pydantic import BaseModel, computed_field


class NiriEvent(BaseModel):
    """Base class for all Niri events.

    Events are asynchronous notifications sent by Niri when state changes.
    """

    @computed_field
    @property
    def name(self) -> str:
        """The name of the event class."""
        return self.__class__.__name__

    @classmethod
    def from_json(cls, line: str, context: Any | None = None) -> "NiriEvent":
        """Parse a JSON line into a NiriEvent instance.

        Args:
            line (str): The JSON string to parse.
            context (Any | None): Validation context (e.g., instance reference).

        Returns:
            NiriEvent: The parsed event instance.

        Raises:
            ValueError: If the event type is unknown.
        """
        data = json.loads(line)
        event_name, payload = next(iter(data.items()))

        subclass = next(
            (c for c in cls.__subclasses__() if c.__name__ == event_name), None
        )
        if subclass is None:
            raise ValueError(f"Unknown event '{event_name}'")

        return subclass.model_validate(payload, context=context)


class WorkspacesChanged(NiriEvent):
    """The [workspace configuration][1] has changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WorkspacesChanged

    Attributes:
        workspaces (list[Workspace]): The new workspace configuration.
            This configuration completely replaces the previous configuration.
            I.e. if any workspaces are missing from here, then they were deleted.
    """

    workspaces: list[Workspace]


class WorkspaceUrgencyChanged(NiriEvent):
    """The [workspace urgency][1] changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WorkspaceUrgencyChanged

    Attributes:
        id (int): Id of the workspace.
        urgent (bool): Whether this workspace has an urgent window.
    """

    id: int
    urgent: bool


class WorkspaceActivated(NiriEvent):
    """A workspace was [activated][1] on an output.

    This doesn’t always mean the workspace became focused, just that it’s now the
    active workspace on its output. All other workspaces on the same output become inactive.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WorkspaceActivated

    Attributes:
        id (int): Id of the newly active workspace.
        focused (bool): Whether this workspace also became focused.
            If `True`, this is now the single focused workspace. All other workspaces
            are no longer focused, but they may remain active on their respective outputs.
    """

    id: int
    focused: bool


class WorkspaceActiveWindowChanged(NiriEvent):
    """An [active window][1] changed on a workspace.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WorkspaceActiveWindowChanged

    Attributes:
        workspace_id (int): Id of the workspace on which the active window changed.
        active_window_id (Optional[int]): Id of the new active window, if any.
    """

    workspace_id: int
    active_window_id: Optional[int]


class WindowsChanged(NiriEvent):
    """The [window configuration][1] has changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WindowsChanged

    Attributes:
        windows (list[Window]): The new window configuration.
            This configuration completely replaces the previous configuration.
            I.e. if any windows are missing from here, then they were closed.
    """

    windows: list[Window]


class WindowOpenedOrChanged(NiriEvent):
    """A new toplevel window was [opened][1], or an existing toplevel window changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WindowOpenedOrChanged

    Attributes:
        window (Window): The new or updated window.
            If the window is focused, all other windows are no longer focused.
    """

    window: Window


class WindowClosed(NiriEvent):
    """A toplevel window was [closed][1].

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WindowClosed

    Attributes:
        id (int): Id of the removed window.
    """

    id: int


class WindowFocusChanged(NiriEvent):
    """Window [focus][1] changed.

    All other windows are no longer focused.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WindowFocusChanged

    Attributes:
        id (Optional[int]): Id of the newly focused window, or `None` if no window is now focused.
    """

    id: Optional[int]


class WindowFocusTimestampChanged(NiriEvent):
    """Window [focus timestamp][1] changed.

    This event is separate from `WindowFocusChanged` because the focus timestamp only
    updates after some debounce time so that quick window switching doesn’t mark
    intermediate windows as recently focused.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WindowFocusTimestampChanged

    Attributes:
        id (int): Id of the window.
        focus_timestamp (Optional[Timestamp]): The new focus timestamp.
    """

    id: int
    focus_timestamp: Optional[Timestamp]


class WindowUrgencyChanged(NiriEvent):
    """Window [urgency][1] changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WindowUrgencyChanged

    Attributes:
        id (int): Id of the window.
        urgent (bool): The new urgency state of the window.
    """

    id: int
    urgent: bool


class WindowLayoutsChanged(NiriEvent):
    """The [layout][1] of one or more windows has changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.WindowLayoutsChanged

    Attributes:
        changes (list[tuple[int, WindowLayout]]): Pairs consisting of a window id and new layout information for the window.
    """

    changes: list[tuple[int, WindowLayout]]


class KeyboardLayoutsChanged(NiriEvent):
    """The configured [keyboard layouts][1] have changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.KeyboardLayoutsChanged

    Attributes:
        keyboard_layouts (KeyboardLayouts): The new keyboard layout configuration.
    """

    keyboard_layouts: KeyboardLayouts


class KeyboardLayoutSwitched(NiriEvent):
    """The [keyboard layout][1] switched.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.KeyboardLayoutSwitched

    Attributes:
        idx (int): Index of the newly active layout.
    """

    idx: int


class OverviewOpenedOrClosed(NiriEvent):
    """The [overview][1] was opened or closed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.OverviewOpenedOrClosed

    Attributes:
        is_open (bool): The new state of the overview.
    """

    is_open: bool


class ConfigLoaded(NiriEvent):
    """The [configuration][1] was reloaded.

    You will always receive this event when connecting to the event stream,
    indicating the last config load attempt.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.ConfigLoaded

    Attributes:
        failed (bool): Whether the loading failed.
            For example, the config file couldn’t be parsed.
    """

    failed: bool


class ScreenshotCaptured(NiriEvent):
    """A [screenshot][1] was captured.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html#variant.ScreenshotCaptured

    Attributes:
        path (Optional[str]): The file path where the screenshot was saved, if it was written to disk.
            If `None`, the screenshot was either only copied to the clipboard, or the path
            couldn’t be converted to a `String` (e.g. contained invalid UTF-8 bytes).
    """

    path: Optional[str]


class CastsChanged(NiriEvent):
    """The list of active [screen casts][1] changed.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html

    Attributes:
        casts (list[Cast]): The new list of active casts.
    """

    casts: list[Cast]


class CastStartedOrChanged(NiriEvent):
    """A [screen cast][1] started or changed state.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html

    Attributes:
        cast (Cast): The cast that started or changed.
    """

    cast: Cast


class CastStopped(NiriEvent):
    """A [screen cast][1] stopped.

    [1]: https://docs.rs/niri-ipc/25.11.0/niri_ipc/enum.Event.html

    Attributes:
        stream_id (int): The ID of the stream that stopped.
    """

    stream_id: int
