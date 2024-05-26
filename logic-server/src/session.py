from __future__ import annotations

import abc
import dataclasses
import datetime
import json
import logging
import textwrap
import typing
from pathlib import Path

import openai
import dotenv

dotenv.load_dotenv()


class DataAgent:
    def get_services_description(self) -> str:
        return Path("services.json").read_text()

    def invoke_service(self, service: str, arguments: dict) -> typing.Generator[str, None, None]:
        if service == "CLOCK":
            import pytz
            local_tz = pytz.timezone("Europe/Berlin")
            utc_tz = pytz.timezone("UTC")

            yield str({"time": utc_tz.localize(datetime.datetime.utcnow()).astimezone(local_tz).strftime("%d.%m.%Y %H:%M:%S")})
        elif service == "NL2COORD":
            import nl2coord.nl_to_coord

            try:
                desc = arguments["description"]
            except KeyError as e:
                raise InvalidApiCall(
                    'Der API-Aufruf muss das Argument \'description\' enthalten! Beispiel: {"service": <servicename>, "args": {...}}') from e

            try:
                out = nl2coord.nl_to_coord.get_coords(desc)
            except Exception as e:
                yield str({"error": str(e)})
            else:
                if out is None:
                    yield str({"error": "Koordinaten konnten nicht bestimmt werden."})
                else:
                    lat, lon = out
                    yield str({"lat": lat, "lon": lon})

        elif service == "GENERAL_WEATHER":
            import dwd_forecast

            try:
                lat = arguments["lat"]
                lon = arguments["lon"]
                day = arguments["date"]
                attribute = arguments["attribute"]
            except KeyError as e:
                raise InvalidApiCall(
                    'Der API-Aufruf muss die Argumente \'lat\', \'lon\', \'date\' und \'attribute\' enthalten! Beispiel: {"service": <servicename>, "args": {...}}') from e

            if not isinstance(lat, (int, float)):
                raise InvalidApiCall("GENERAL_WEATHER: 'lat' muss eine Zahl sein!")

            if not isinstance(lon, (int, float)):
                raise InvalidApiCall("GENERAL_WEATHER: 'lon' muss eine Zahl sein!")

            if not isinstance(attribute, str):
                raise InvalidApiCall("GENERAL_WEATHER: 'attribute' muss ein String sein!")

            yield str(dwd_forecast.get_weather_forcast(lon, lat, day, attribute))
        elif service == "KLIPS_DRESDEN":
            import klips_json

            try:
                lat = arguments["lat"]
                lon = arguments["lon"]
                date = arguments["datetime"]
            except KeyError as e:
                raise InvalidApiCall(
                    'Der API-Aufruf muss die Argumente \'lat\', \'lon\' und \'datetime\' enthalten! Beispiel: {"service": <servicename>, "args": {...}}') from e

            try:
                date = datetime.datetime.fromisoformat(date)

                # convert date from local time to UTC using pytz
                import pytz
                local_tz = pytz.timezone("Europe/Berlin")
                utc_tz = pytz.timezone("UTC")
                date = local_tz.localize(date).astimezone(utc_tz).replace(tzinfo=None).isoformat()

                yield str([
                    (
                        utc_tz.localize(d).astimezone(local_tz).replace(tzinfo=None).isoformat(),
                        temp
                    ) for d, temp in klips_json.request((lat, lon), date)
                ])
            except Exception as e:
                # raise
                yield str({"error": str(e)})
        elif service == "HITZE_HANDBUCH":
            try:
                prompt = arguments["prompt"]
            except KeyError as e:
                raise InvalidApiCall(
                    'Der API-Aufruf muss die Argumente \'prompt\', enthalten! Beispiel: {"service": <servicename>, "args": {...}}') from e
            try:
                from heat_tips_retrieval.file_retrieval import retrieve_from_file
                yield from retrieve_from_file(None, prompt)
            except Exception as e:
                # raise
                yield str({"error": str(e)})
        else:
            yield str({"error": f"Unknown service {service}"})


class DialogAgent(abc.ABC):
    messages: list[Message]

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
            logging.getLogger("DialogAgent").info(f"SYS> {message}")
        elif role == "user":
            logging.getLogger("DialogAgent").info(f"USR> {message}")
        self.messages.append(Message(role, message))

    def get_response(self) -> typing.Generator[str, None, None]:
        messages_serialized = [
            {"role": message.role, "content": message.content}
            for message in self.messages
        ]

        # noinspection PyTypeChecker
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages_serialized,
            stream=True
        )

        chunks = []
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                chunks.append(chunk.choices[0].delta.content)
                yield chunk.choices[0].delta.content

        self.add_message("".join(chunks), "system")


class InvalidApiCall(Exception):
    ...


@dataclasses.dataclass
class Session:
    data_agent: DataAgent
    dialog_agent: DialogAgent

    def get_response(self, prompt: str, role="user") -> typing.Generator[str, None, None]:
        self.dialog_agent.add_message(prompt, role)

        clock_msg_index = len(self.dialog_agent.messages)
        self.dialog_agent.add_message("{\"service\": \"CLOCK\", \"args\": {}}", "system")
        self.dialog_agent.add_message("API-Antwort: " + "".join(self.data_agent.invoke_service("CLOCK", {})), "system")

        for _ in range(10):
            try:
                response_iterator = self.dialog_agent.get_response()

                for token in response_iterator:
                    if "{" not in token:
                        yield token
                    else:
                        up_to, after = token.split("{", 1)
                        yield up_to
                        break
                else:
                    break

                potential_json = ("{" + after + "".join(response_iterator)).strip("`").strip()

                try:
                    parsed = json.loads(potential_json)
                except (KeyError, json.JSONDecodeError) as e:
                    # raise InvalidApiCall("Du musst valides JSON angeben!") from e
                    self.dialog_agent.messages.pop()
                    continue

                try:
                    service = parsed["service"]
                    args = parsed["args"]
                except KeyError as e:
                    raise InvalidApiCall("Der API-Aufruf muss die Schlüssel 'service' und 'args' enthalten!") from e

                else:
                    result = "API-Antwort: " + "".join(self.data_agent.invoke_service(service, args))

                    self.dialog_agent.add_message(
                        message=json.dumps(result, ensure_ascii=False),
                        role="system"
                    )
            except InvalidApiCall as e:
                self.dialog_agent.add_message(str(e), "system")

        del self.dialog_agent.messages[clock_msg_index:clock_msg_index+2]


def create_session() -> Session:
    data_agent = DataAgent()

    system_prompt = textwrap.dedent(f"""
    Verhalte dich wie ein Berater zum Thema Bewältigung und Umgang mit Hitze. Gib konkrete Handlungsempfehlungen auf Anfragen. Nutze folgende APIs, um deine Anfragen mit spezifischen Daten zu füllen.
    Um eine API auszuführen, beende deine Antwort mit einem JSON in der Form {{"service": "<name der API>", "args": {{<argumente der API>}}}}. BEENDE DANACH DEINE ANTWORT. Frage keine APIs, an wenn der Benutzer nicht nach relevaten Informationen gefragt hat. Folgende APIs stehen dir zur Verfügung:
    {data_agent.get_services_description()}
    Es folgen Beispiele für die API-Aufrufe:
    """ + '{"service": "CLOCK", args: {}}')

    hints = textwrap.dedent("""
    Folge Dinge sind zu beachten:
    - Gib knappe, aber präzise Antworten, als würdest du ein Telefongespräch führen.
    - Kündige deine Aktionen nicht an. Wenn du eine API aufrufen möchtest, tu es zu Beginn deiner Nachricht. Schreibe keinen Text davor.
    - Frage NIEMALS, ob du spezifische APIs nutzen sollst, sondern NUTZE SIE. Denke dir KEINE Temperaturen, Witterungsbedingungen oder Koordinaten aus.
    - Denke dir keine Hitze-Tipps auf, die du in der HITZE_HANDBUCH-API finden kannst.
    - Falls kein Datum angegeben wurde, nimm heute an.
    - Nenne NIEMALS APIs beim Namen.
    - Vermeide Wiederholungen
    - Benutze stets die Höflichkeitsanrede, außer dir wird das Du angeboten.
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
                content="API-Antwort: " + str(data_agent.invoke_service("CLOCK", {}))
            ),
            Message(
                role="system",
                content=hints
            )
        ]
    )

    return Session(data_agent, dialog_agent)
