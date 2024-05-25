from __future__ import annotations

import abc
import dataclasses
import datetime
import json
import textwrap
import typing
from pathlib import Path

import openai
import dotenv

dotenv.load_dotenv()


class DataAgent:
    def get_services_description(self) -> str:
        return Path("services.json").read_text()

    def invoke_service(self, service: str, arguments: dict) -> dict | list:
        if service == "CLOCK":
            return {"time": datetime.datetime.now().isoformat()}
        elif service == "NL2COORD":
            import nl2coord.nl_to_coord

            try:
                desc = arguments["description"]
            except KeyError as e:
                raise InvalidApiCall(
                    'Der API-Aufruf muss das Argument \'description\' enthalten! Beispiel: {"service": <servicename>, "args": {...}}') from e

            lat, lon = nl2coord.nl_to_coord.get_coords(desc)

            return {"lat": lat, "lon": lon}

        elif service == "COARSE_TEMPERATURE":
            import dwd_forecast

            try:
                lat = arguments["lat"]
                lon = arguments["lon"]
                day = arguments["date"]
                attribute = arguments["attribute"]
            except KeyError as e:
                raise InvalidApiCall(
                    'Der API-Aufruf muss die Argumente \'lat\', \'lon\', \'date\' und \'attribute\' enthalten! Beispiel: {"service": <servicename>, "args": {...}}') from e

            return dwd_forecast.get_weather_forcast(lon, lat, day, attribute)

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
    model: str = "gpt-4o"

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


class InvalidApiCall(Exception):
    ...


@dataclasses.dataclass
class Session:
    data_agent: DataAgent
    dialog_agent: DialogAgent

    def get_response(self, prompt: str) -> str:
        self.dialog_agent.add_message(prompt, "user")

        out_messages = []

        while True:
            try:
                response = self.dialog_agent.get_response().strip()

                if "{" in response:
                    message, potential_json = response.split("{", 1)
                    potential_json = "{" + potential_json
                    potential_json = potential_json.strip("`").strip()

                    message = message.strip()
                    if message:
                        out_messages.append(message)

                    try:
                        parsed = json.loads(potential_json)
                    except (KeyError, json.JSONDecodeError) as e:
                        raise InvalidApiCall("Du musst valides JSON angeben!") from e

                    try:
                        service = parsed["service"]
                        args = parsed["args"]
                    except KeyError as e:
                        raise InvalidApiCall("Der API-Aufruf muss die Schlüssel 'service' und 'args' enthalten!") from e

                    else:
                        result = self.data_agent.invoke_service(service, args)

                        self.dialog_agent.add_message(
                            message=json.dumps(result, ensure_ascii=False),
                            role="system"
                        )
                else:
                    out_messages.append(response)
                    break
            except InvalidApiCall as e:
                self.dialog_agent.add_message(str(e), "system")

        return "\n\n".join(out_messages)


def create_session() -> Session:
    data_agent = DataAgent()

    system_prompt = textwrap.dedent(f"""
    Verhalte dich wie ein Berater zum Thema Bewältigung und Umgang mit Hitze. Gib konkrete Handlungsempfehlungen auf Anfragen. Nutze folgende APIs, um deine Anfragen mit spezifischen Daten zu füllen.
    Um eine API auszuführen, antworte NUR mit dem Namen der API sowie den Argumenten in JSON-Form. Beende danach deine Antwort. Frage keine APIs, an wenn der Benutzer nicht nach relevaten Informationen gefragt hat. Folgende APIs stehen dir zur Verfügung:
    {data_agent.get_services_description()}
    Es folgen Beispiele für die API-Aufrufe:
    """ + '{"service": "CLOCK", args: {}}')

    hints = textwrap.dedent("""
    Folge Dinge sind zu beachten:
    - Befrage die CLOCK-API JEDES MAL, wenn dich der Benutzer nach einer Uhrzeit fragt. Benutze NIEMALS Rückgaben der CLOCK-API, die älter sind als eine Anfrage des Benutzers.
    - Gib knappe, aber präzise Antworten, als würdest du ein Telefongespräch führen.
    - Kündige deine Aktionen nicht an. Wenn du eine API aufrufen möchtest, tu es zu beginn deiner Nachricht. Schreibe keinen Text davor.
    - Frage nicht, ob du spezifische APIs nutzen sollst. Nutze sie einfach, und entscheide, ob sie relevant für deine Antwort sind.
    """)

    dialog_agent = OpenAiDialogAgent(
        openai_client=openai.Client(),
        messages=[
            Message(
                role="system",
                content=system_prompt
            ),
            Message(
                role="system",
                content=str(data_agent.invoke_service("CLOCK", {}))
            ),
            Message(
                role="system",
                content=hints
            )
        ]
    )

    return Session(data_agent, dialog_agent)
