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

    def _create_model_with_instance(self, model: type[T], data: dict):
        m = model(**data)
        m._instance = self
        return m

    def get_windows(self) -> list[Window]:
        windows: list[dict] = json.loads(
            self.socket.send_command('{"Windows": null}\n')
        )["Ok"]["Windows"]
        return [self._create_model_with_instance(Window, w) for w in windows]

    def get_workspaces(self) -> list[Workspace]:
        workspaces: list[dict] = json.loads(
            self.socket.send_command('{"Workspaces": null}\n')
        )["Ok"]["Workspaces"]
        return [self._create_model_with_instance(Workspace, ws) for ws in workspaces]

    def get_outputs(self) -> list[Output]:
        outputs: dict = json.loads(self.socket.send_command('{"Outputs": null}\n'))[
            "Ok"
        ]["Outputs"]
        return [self._create_model_with_instance(Output, o) for o in outputs.values()]

    def get_layers(self) -> list[LayerSurface]:
        layers: list[dict] = json.loads(self.socket.send_command('{"Layers": null}\n'))[
            "Ok"
        ]["Layers"]
        return [self._create_model_with_instance(LayerSurface, l) for l in layers]

    # def action(self, arguments: list[str]):
    #     response = self.socket.send_command("action", flags=["-j"], args=arguments)
    #     return response if response != "ok" else None
