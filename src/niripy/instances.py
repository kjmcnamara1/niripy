import json
from typing import TypeVar

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


class Instance:
    socket: Socket
    version: str

    def __init__(self):
        self.socket = Socket()
        self.version = self._request("version").version or "unknown"

    def __repr__(self) -> str:
        return f"<Instance(socket={str(self.socket.path)!r})>"

    def _request(self, command: str, *args: str) -> Response:
        # to_snake is needed to convert from kebab-case
        command = to_pascal(to_snake(command))
        reply = Reply.model_validate_json(
            self.socket.send_command(f'{{"{command}": null}}\n')
        )
        return reply.unwrap()

    ## def _create_model_with_instance(self, model: type[T], data: dict) -> T:
    ##     m = model(**data)
    ##     m._instance = self
    ##     return m

    def _add_instance_to_model(self, model: T) -> T:
        model._instance = self
        return model

    def get_windows(self) -> list[Window]:
        windows = self._request("windows").windows or []
        return [self._add_instance_to_model(window) for window in windows]

    def get_focused_window(self) -> Window:
        focused_window = self._request("focused-window").focused_window
        if focused_window is None:
            raise ValueError("No focused window")
        return self._add_instance_to_model(focused_window)

    def get_workspaces(self) -> list[Workspace]:
        workspaces = self._request("workspaces").workspaces or []
        return [self._add_instance_to_model(workspace) for workspace in workspaces]

    def get_focused_workspace(self) -> Workspace:
        focused_workspace = next(
            (ws for ws in self.get_workspaces() if ws.is_focused), None
        )
        if focused_workspace is None:
            raise ValueError("No focused workspace")
        return self._add_instance_to_model(focused_workspace)

    def get_outputs(self) -> list[Output]:
        outputs = self._request("outputs").outputs or {}
        return [self._add_instance_to_model(output) for output in outputs.values()]

    def get_focused_output(self) -> Output:
        focused_output = self._request("focused-output").focused_output
        if focused_output is None:
            raise ValueError("No focused output")
        return self._add_instance_to_model(focused_output)

    def get_layers(self) -> list[LayerSurface]:
        layers = self._request("layers").layers or []
        return [self._add_instance_to_model(layer) for layer in layers]

    # def action(self, arguments: list[str]):
    #     response = self.socket.send_command("action", flags=["-j"], args=arguments)
    #     return response if response != "ok" else None
