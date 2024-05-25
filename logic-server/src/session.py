from __future__ import annotations

import abc
import dataclasses
import datetime
import json
import textwrap
import typing
from pathlib import Path

import openai


class DataAgent:
    def get_services_description(self) -> str:
        return Path("services.json").read_text()

    def invoke_service(self, service: str, arguments: dict) -> dict:
        if service == "CLOCK":
            return {"time": datetime.datetime.now().isoformat()}
        else:
            return {"error": f"Unknown service {service}"}


class DialogAgent(abc.ABC):
    @abc.abstractmethod
    def add_message(self, message: str, role: typing.Literal["user", "system"]):
        ...

    @abc.abstractmethod
    def get_response(self) -> str:
        ...


@dataclasses.dataclass
class Message:
    role: str
    content: str


@dataclasses.dataclass
class OpenAiDialogAgent(DialogAgent):
    openai_client: openai.Client
    model: str = "gpt-3.5-turbo"

    messages: list[Message] = dataclasses.field(default_factory=list)

    def add_message(self, message: str, role: str):
        if role == "system":
            print(f"SYS> {message}")
        elif role == "user":
            print(f"USR> {message}")
        self.messages.append(Message(role, message))

    def get_response(self) -> str:
        messages_serialized = [
            {"role": message.role, "content": message.content}
            for message in self.messages
        ]

        # noinspection PyTypeChecker
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages_serialized
        )

        msg = response.choices[0].message
        self.add_message(msg.content, "system")

        return msg.content


datetime.datetime.strptime("2024-05-01 06:00:00", "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=2)


@dataclasses.dataclass
class Session:
    data_agent: DataAgent
    dialog_agent: DialogAgent

    def get_response(self, prompt: str) -> str:
        self.dialog_agent.add_message(prompt, "user")
        response = self.dialog_agent.get_response().strip()

        if "{" in response:
            potential_json = response[response.index("{"):]
            print("LLM responded with service call...", potential_json)
            try:
                parsed = json.loads(potential_json)

                service = parsed["service"]
                args = parsed["args"]
            except (KeyError, json.JSONDecodeError):
                return f"Invalid service call {response}"
            else:
                result = self.data_agent.invoke_service(service, args)

                self.dialog_agent.add_message(
                    message=json.dumps(result, ensure_ascii=False),
                    role="system"
                )

            return self.dialog_agent.get_response()
        else:
            return response
