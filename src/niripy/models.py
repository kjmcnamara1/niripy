from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_pascal

if TYPE_CHECKING:
    from niripy.instances import Instance


class ReplyError(Exception):
    """Exception raised when an error occurs while processing a reply."""

    pass


class ModelWithInstance(BaseModel):
    _instance: "Instance"

    def model_post_init(self, context: Any):
        if not isinstance(context, dict) or "instance" not in context:
            raise AssertionError(
                "context['instance'] not defined: Make sure to validate with context={'instance': ...}. "
                "i.e. Model.model_validate(data, context={'instance': instance})"
            )
        self._instance = context["instance"]


class ConfiguredPosition(BaseModel):
    x: int
    y: int


class KeyboardLayouts(BaseModel):
    names: list[str]
    current_idx: int


class Layer(StrEnum):
    BACKGROUND = "Background"
    BOTTOM = "Bottom"
    TOP = "Top"
    OVERLAY = "Overlay"


class LayerSurfaceKeyboardInteractivity(StrEnum):
    NONE = "None"
    EXCLUSIVE = "Exclusive"
    ON_DEMAND = "OnDemand"


class LayerSurface(ModelWithInstance):
    namespace: str
    output: str
    layer: Layer
    keyboard_interactivity: LayerSurfaceKeyboardInteractivity


class Transform(StrEnum):
    NORMAL = "Normal"
    ROTATE_90 = "_90"
    ROTATE_180 = "_180"
    ROTATE_270 = "_270"
    FLIPPED = "Flipped"
    FLIPPED_90 = "Flipped90"
    FLIPPED_180 = "Flipped180"
    FLIPPED_270 = "Flipped270"


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


class Output(ModelWithInstance):
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

    @property
    def workspaces(self):
        return [ws for ws in self._instance.get_workspaces() if ws.output == self.name]

    @property
    def layers(self):
        return [
            layer for layer in self._instance.get_layers() if layer.output == self.name
        ]

    @property
    def windows(self):
        workspace_ids = [ws.id for ws in self.workspaces]
        return [
            window
            for window in self._instance.get_windows()
            if window.workspace_id in workspace_ids
        ]


class Overview(BaseModel):
    is_open: bool


# [ ]: test colorpicker
class PickedColor(BaseModel):
    rgb: tuple[float, float, float]


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
    output_name: str | None = Field(alias="output")
    is_urgent: bool
    is_active: bool
    is_focused: bool
    active_window_id: int | None

    @property
    def output(self) -> Output | None:
        if self.output_name is None:
            return None
        return self._instance.get_output_by_name(self.output_name)

    @property
    def active_window(self) -> Window | None:
        if self.active_window_id is None:
            return None
        return self._instance.get_window_by_id(self.active_window_id)

    @property
    def windows(self) -> list[Window]:
        return [
            window
            for window in self._instance.get_windows()
            if window.workspace_id == self.id
        ]


class OutputConfigChanged(StrEnum):
    APPLIED = "Applied"
    OUTPUT_WAS_MISSING = "OutputWasMissing"


class CastKind(StrEnum):
    PIPEWIRE = "PipeWire"
    WLR_SCREENCOPY = "WlrScreencopy"


class CastTarget(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)
    nothing: dict | None = None
    output: dict[str, str] | None = None
    window: dict[str, int] | None = None


# [ ]: test screencasting
class Cast(BaseModel):
    stream_id: int
    session_id: int
    kind: CastKind
    target: CastTarget
    is_dynamic_target: bool
    is_active: bool
    pid: int | None
    pw_node_id: int | None


class Response(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)
    version: str | None = None
    outputs: dict[str, Output] | None = None
    workspaces: list[Workspace] | None = None
    windows: list[Window] | None = None
    layers: list[LayerSurface] | None = None
    keyboard_layouts: KeyboardLayouts | None = None
    focused_output: Output | None = None
    focused_window: Window | None = None
    picked_window: Window | None = None
    picked_color: PickedColor | None = None
    output_config_changed: OutputConfigChanged | None = None
    overview_state: Overview | None = None
    casts: list[Cast] | None = None


class Reply(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal)
    ok: Response | None = None
    err: str | None = None

    def unwrap(self) -> Response:
        if self.err is not None:
            raise ReplyError(f"Niri replied with error: {self.err}")
        assert self.ok is not None
        return self.ok


# class Action(BaseModel):
#     name: str
