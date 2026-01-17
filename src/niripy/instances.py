import json
from typing import TypeVar

from niripy.models import ModelWithInstance, Window, Workspace
from niripy.sockets import Socket

T = TypeVar("T", bound=ModelWithInstance)


class Instance:
    socket: Socket

    def __init__(self):
        self.socket = Socket()

    def _create_model_with_instance(self, model: type[T], data: dict):
        m = model(**data)
        m._instance = self
        return m

    def get_windows(self) -> list[Window]:
        windows: list[dict] = json.loads(
            self.socket.send_command('{"Windows": null}\n')
        )["Ok"]["Windows"]
        # print(json.dumps(windows_data, indent=4))
        return [self._create_model_with_instance(Window, w) for w in windows]

    def get_workspaces(self) -> list[Workspace]:
        workspaces: list[dict] = json.loads(
            self.socket.send_command('{"Workspaces": null}\n')
        )["Ok"]["Workspaces"]
        return [self._create_model_with_instance(Workspace, ws) for ws in workspaces]

    # def action(self, arguments: list[str]):
    #     response = self.socket.send_command("action", flags=["-j"], args=arguments)
    #     return response if response != "ok" else None
