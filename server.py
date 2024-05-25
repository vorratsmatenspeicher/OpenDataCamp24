import openai
from flask import Flask, request

import session

app = Flask(__name__)

SESSIONS: dict[str, session.Session] = {}


@app.route("/create_session")
def create_session():
    i = 0
    while f"session_{i}" in SESSIONS:
        i += 1

    location_determiner = session.DataAgent()
    dialog_agent = session.OpenAiDialogAgent(
        openai_client=openai.Client(),
        messages=[session.Message(
            role="system",
            content="""Verhalte dich wie ein Berater zum Thema Bewältigung und Umgang mit Hitze. Gib konkrete Handlungsempfehlungen auf Anfragen. Nutze folgende APIs, um deine Anfragen mit spezifischen Daten zu füllen.
Um eine API auszuführen, antworte NUR mit dem Namen der API sowie den Argumenten in JSON-Form. Beende danach deine Antwort. Folgende APIs stehen dir zur Verfügung:

Heute ist der 2024-05-25.

1)
Name: GET_COORDINATES
Beschreibung: Ermittelt aus der Beschreibung eines Ortes die geographischen Koordinaten.
Beispielargumente: {"description": "Der Bäcker hinter dem Rathaus"}
Beispielergebnis: {"lat": 23.2352, "lon": 7.2342}

2)
Name: GET_WEATHER
Beschreibung: Gibt die aktuellen und prognostizierten Wetterdaten für einen Standort zurück.
Beispielargumente: {"lat": 23.2352, "lon": 7.2342}
Beispielergebnis: [{"date": "2024-05-25": {"temp": 45, "humidity": 99}}]"""
        )]
    )
    SESSIONS[f"session_{i}"] = session.Session(location_determiner, dialog_agent)

    return {"session_id": f"session_{i}"}


def error(message: str):
    return {"error": message}


@app.route("/get_response")
def get_response():
    if "session_id" not in request.args:
        return error("session_id is required")

    if "prompt" not in request.args:
        return error("prompt is required")

    session_id = request.args["session_id"]

    if session_id not in SESSIONS:
        return error("Invalid session_id")

    return {"response": SESSIONS[session_id].get_response(request.args["prompt"])}


if __name__ == '__main__':
    app.run(debug=True)
