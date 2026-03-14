import json

from typing import Optional, Any

from niripy.models import Workspace, Window, WindowLayout, KeyboardLayouts, Cast, Timestamp
from pydantic import BaseModel, computed_field

class NiriEvent(BaseModel):
    @computed_field
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @classmethod
    def from_json(cls, line: str, context: Any | None = None) -> "NiriEvent":
        data = json.loads(line)
        event_name, payload = next(iter(data.items()))

        subclass = next(
            (c for c in cls.__subclasses__() if c.__name__ == event_name),
            None
        )
        if subclass is None:
            raise ValueError(f"Unknown event '{event_name}'")

        return subclass.model_validate(payload, context=context)


class WorkspacesChanged(NiriEvent):
    workspaces: list[Workspace]

class WorkspaceUrgencyChanged(NiriEvent):
    id: int
    urgent: bool

class WorkspaceActivated(NiriEvent):
    id: int
    focused: bool

class WorkspaceActiveWindowChanged(NiriEvent):
    workspace_id: int
    active_window_id: Optional[int]

class WindowsChanged(NiriEvent):
    windows: list[Window]

class WindowOpenedOrChanged(NiriEvent):
    window: Window

class WindowClosed(NiriEvent):
    id: int

class WindowFocusChanged(NiriEvent):
    id: Optional[int]

class WindowFocusTimestampChanged(NiriEvent):
    id: int
    focus_timestamp: Optional[Timestamp]

class WindowUrgencyChanged(NiriEvent):
    id: int
    urgent: bool

class WindowLayoutsChanged(NiriEvent):
    changes: list[tuple[int, WindowLayout]]

class KeyboardLayoutsChanged(NiriEvent):
    keyboard_layouts: KeyboardLayouts

class KeyboardLayoutSwitched(NiriEvent):
    idx: int

class OverviewOpenedOrClosed(NiriEvent):
    is_open: bool

class ConfigLoaded(NiriEvent):
    failed: bool

class ScreenshotCaptured(NiriEvent):
    path: Optional[str]

class CastsChanged(NiriEvent):
    casts: list[Cast]

class CastStartedOrChanged(NiriEvent):
    cast: Cast

class CastStopped(NiriEvent):
    stream_id: int