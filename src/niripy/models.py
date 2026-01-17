from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from niripy.instances import Instance


class ModelWithInstance(BaseModel):
    _instance: "Instance"


class ConfiguredPosition(BaseModel):
    x: int
    y: int


class KeyboardLayouts(BaseModel):
    names: list[str]
    current_idx: int


class Layer(Enum):
    BACKGROUND = "background"
    BOTTOM = "bottom"
    TOP = "top"
    OVERLAY = "overlay"


class LayerSurfaceKeyboardInteractivity(Enum):
    NONE = "none"
    EXCLUSIVE = "exclusive"
    ON_DEMAND = "on_demand"


class LayerSurface(BaseModel):
    namespace: str
    output: str
    layer: Layer
    keyboard_interactivity: LayerSurfaceKeyboardInteractivity


# ? Maybe StrEnum?
class Transform(Enum):
    NORMAL = "normal"
    ROTATE_90 = "rotate-90"
    ROTATE_180 = "rotate-180"
    ROTATE_270 = "rotate-270"
    FLIPPED = "flipped"
    FLIPPED_90 = "flipped-90"
    FLIPPED_180 = "flipped-180"
    FLIPPED_270 = "flipped-270"


class LogicalOutput(BaseModel):
    x: int
    y: int
    width: int
    height: int
    scale: float
    transform: Transform


class Mode(BaseModel):
    width: int
    height: int
    refresh_rate: int
    is_preferred: bool


class Output(BaseModel):
    name: str
    make: str
    model: str
    serial: str | None
    physical_size: tuple[int, int]
    modes: list[Mode]
    current_mode: int | None
    is_custom_mode: bool
    vrr_supported: bool
    vrr_enabled: bool
    logical: LogicalOutput | None


class Overview(BaseModel):
    is_open: bool


# class PickedColor(BaseModel):


class Timestamp(BaseModel):
    seconds: int = Field(alias="secs")
    nanoseconds: int = Field(alias="nanos")


class VrrToSet(BaseModel):
    vrr: bool
    on_demand: bool


class WindowLayout(BaseModel):
    pos_in_scrolling_layout: tuple[int, int] | None
    tile_size: tuple[float, float]
    window_size: tuple[int, int]
    tile_pos_in_workspace_view: tuple[float, float] | None
    window_offset_in_tile: tuple[float, float]


class Window(ModelWithInstance):
    id: int
    title: str | None
    app_id: str | None
    pid: int | None
    workspace_id: int | None
    is_focused: bool
    is_floating: bool
    is_urgent: bool
    layout: WindowLayout
    focus_timestamp: Timestamp | None


class Workspace(ModelWithInstance):
    id: int
    idx: int
    name: str | None
    output: str | None
    is_urgent: bool
    is_active: bool
    is_focused: bool
    active_window_id: int | None


# class Action(BaseModel):
#     name: str
