import abc
import dataclasses
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


@dataclasses.dataclass
class Session:
    location_determiner: LocationDeterminer
    dialog_agent: DialogAgent

    def get_response(self, prompt: str) -> str:
        response = self.dialog_agent.get_response(prompt)


