import json
from typing import Any, Literal, TypeVar

from icecream import ic
from pydantic.alias_generators import to_pascal, to_snake

from niripy.models import (
    LayerSurface,
    ModelWithInstance,
    Output,
    Reply,
    Response,
    Window,
    Workspace,
)
from niripy.sockets import Socket

T = TypeVar("T", bound=ModelWithInstance)

RequestCmd = Literal[
    "outputs",
    "workspaces",
    "windows",
    "layers",
    "keyboard-layouts",
    "focused-output",
    "focused-window",
    "pick-window",
    "pick-color",
    "version",
    "request-error",
    "overview-state",
]

ActionCmd = Literal[
    "quit",
    "power-off-monitors",
    "power-on-monitors",
    "spawn",
    "spawn-sh",
    "do-screen-transition",
    "screenshot",
    "screenshot-screen",
    "screenshot-window",
    "toggle-keyboard-shortcuts-inhibit",
    "close-window",
    "fullscreen-window",
    "toggle-windowed-fullscreen",
    "focus-window",
    "focus-window-in-column",
    "focus-window-previous",
    "focus-column-left",
    "focus-column-right",
    "focus-column-first",
    "focus-column-last",
    "focus-column-right-or-first",
    "focus-column-left-or-last",
    "focus-column",
    "focus-window-or-monitor-up",
    "focus-window-or-monitor-down",
    "focus-column-or-monitor-left",
    "focus-column-or-monitor-right",
    "focus-window-down",
    "focus-window-up",
    "focus-window-down-or-column-left",
    "focus-window-down-or-column-right",
    "focus-window-up-or-column-left",
    "focus-window-up-or-column-right",
    "focus-window-or-workspace-down",
    "focus-window-or-workspace-up",
    "focus-window-top",
    "focus-window-bottom",
    "focus-window-down-or-top",
    "focus-window-up-or-bottom",
    "move-column-left",
    "move-column-right",
    "move-column-to-first",
    "move-column-to-last",
    "move-column-left-or-to-monitor-left",
    "move-column-right-or-to-monitor-right",
    "move-column-to-index",
    "move-window-down",
    "move-window-up",
    "move-window-down-or-to-workspace-down",
    "move-window-up-or-to-workspace-up",
    "consume-or-expel-window-left",
    "consume-or-expel-window-right",
    "consume-window-into-column",
    "expel-window-from-column",
    "swap-window-right",
    "swap-window-left",
    "toggle-column-tabbed-display",
    "set-column-display",
    "center-column",
    "center-window",
    "center-visible-columns",
    "focus-workspace-down",
    "focus-workspace-up",
    "focus-workspace",
    "focus-workspace-previous",
    "move-window-to-workspace-down",
    "move-window-to-workspace-up",
    "move-window-to-workspace",
    "move-column-to-workspace-down",
    "move-column-to-workspace-up",
    "move-column-to-workspace",
    "move-workspace-down",
    "move-workspace-up",
    "move-workspace-to-index",
    "set-workspace-name",
    "unset-workspace-name",
    "focus-monitor-left",
    "focus-monitor-right",
    "focus-monitor-down",
    "focus-monitor-up",
    "focus-monitor-previous",
    "focus-monitor-next",
    "focus-monitor",
    "move-window-to-monitor-left",
    "move-window-to-monitor-right",
    "move-window-to-monitor-down",
    "move-window-to-monitor-up",
    "move-window-to-monitor-previous",
    "move-window-to-monitor-next",
    "move-window-to-monitor",
    "move-column-to-monitor-left",
    "move-column-to-monitor-right",
    "move-column-to-monitor-down",
    "move-column-to-monitor-up",
    "move-column-to-monitor-previous",
    "move-column-to-monitor-next",
    "move-column-to-monitor",
    "set-window-width",
    "set-window-height",
    "reset-window-height",
    "switch-preset-column-width",
    "switch-preset-column-width-back",
    "switch-preset-window-width",
    "switch-preset-window-width-back",
    "switch-preset-window-height",
    "switch-preset-window-height-back",
    "maximize-column",
    "maximize-window-to-edges",
    "set-column-width",
    "expand-column-to-available-width",
    "switch-layout",
    "show-hotkey-overlay",
    "move-workspace-to-monitor-left",
    "move-workspace-to-monitor-right",
    "move-workspace-to-monitor-down",
    "move-workspace-to-monitor-up",
    "move-workspace-to-monitor-previous",
    "move-workspace-to-monitor-next",
    "move-workspace-to-monitor",
    "toggle-debug-tint",
    "debug-toggle-opaque-regions",
    "debug-toggle-damage",
    "toggle-window-floating",
    "move-window-to-floating",
    "move-window-to-tiling",
    "focus-floating",
    "focus-tiling",
    "switch-focus-between-floating-and-tiling",
    "move-floating-window",
    "toggle-window-rule-opacity",
    "set-dynamic-cast-window",
    "set-dynamic-cast-monitor",
    "clear-dynamic-cast-target",
    "toggle-overview",
    "open-overview",
    "close-overview",
    "toggle-window-urgent",
    "set-window-urgent",
    "unset-window-urgent",
    "load-config-file",
]


def kebab_to_pascal(s: str) -> str:
    return to_pascal(to_snake(s))


class Instance:
    socket: Socket
    version: str

    def __init__(self):
        self.socket = Socket()
        self.version = self._request("version").version or "unknown"

    def __repr__(self) -> str:
        return f"<Instance(socket={str(self.socket.path)!r})>"

    def _request(self, command: RequestCmd) -> Response:
        command_str = kebab_to_pascal(command)
        reply = Reply.model_validate_json(
            self.socket.send_command(command_str),
            context={"instance": self},
        )
        return reply.unwrap()

    def action(self, action: ActionCmd, **kwargs: Any) -> bool:
        action_str = kebab_to_pascal(action)
        request = {"Action": {action_str: {}}}
        for k, v in kwargs.items():
            request["Action"][action_str].update({k: v})
        reply = Reply.model_validate_json(
            self.socket.send_command(request),
            context={"instance": self},
        )
        return reply.unwrap().handled or False

    def get_windows(self) -> list[Window]:
        return self._request("windows").windows or []

    def get_focused_window(self) -> Window:
        focused_window = self._request("focused-window").focused_window
        if focused_window is None:
            raise ValueError("Unable to retrieve focused window")
        return focused_window

    def get_window_by_id(self, window_id: int) -> Window | None:
        for window in self.get_windows():
            if window.id == window_id:
                return window

    def get_workspaces(self) -> list[Workspace]:
        return self._request("workspaces").workspaces or []

    def get_focused_workspace(self) -> Workspace:
        focused_workspace = next(
            (ws for ws in self.get_workspaces() if ws.is_focused), None
        )
        if focused_workspace is None:
            raise ValueError("Unable to retrieve focused workspace")
        return focused_workspace

    def get_workspace_by_id(self, workspace_id: int) -> Workspace | None:
        for workspace in self.get_workspaces():
            if workspace.id == workspace_id:
                return workspace

    def get_workspace_by_name(self, name: str) -> Workspace | None:
        for workspace in self.get_workspaces():
            if workspace.name == name:
                return workspace

    def get_outputs(self) -> list[Output]:
        return list((self._request("outputs").outputs or {}).values())

    def get_focused_output(self) -> Output:
        focused_output = self._request("focused-output").focused_output
        if focused_output is None:
            raise ValueError("Unable to retrieve focused output")
        return focused_output

    def get_output_by_name(self, name: str) -> Output | None:
        outputs = self._request("outputs").outputs or {}
        return outputs.get(name)

    def get_layers(self) -> list[LayerSurface]:
        return self._request("layers").layers or []
