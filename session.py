import abc
import dataclasses
import json
import typing


class LocationDeterminer(abc.ABC):
    @abc.abstractmethod
    def determine_location(self, description: str):
        ...


class DialogAgent(abc.ABC):
    @abc.abstractmethod
    def add_message(self, message: str, role: typing.Literal["user", "system"]):
        ...

    @abc.abstractmethod
    def get_response(self) -> str:
        ...


JSON_KEYWORD = "CALL_DATA_AGENT"


@dataclasses.dataclass
class Session:
    location_determiner: LocationDeterminer
    dialog_agent: DialogAgent

    def get_response(self, prompt: str) -> str:
        self.dialog_agent.add_message(prompt, "user")
        response = self.dialog_agent.get_response()

        if response.startswith(JSON_KEYWORD):
            data = json.loads(response[len(JSON_KEYWORD):])
            location = self.location_determiner.determine_location(data["description"])
            self.dialog_agent.add_message(f"Location: {location}", "system")

        return self.dialog_agent.get_response()
