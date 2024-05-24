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

    location_determiner = session.LocationDeterminer()
    dialog_agent = session.OpenAiDialogAgent(
        openai_client=openai.Client(),
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
