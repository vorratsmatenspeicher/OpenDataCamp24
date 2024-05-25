import logging
import sys
import openai
from flask import Flask, request

import session

app = Flask(__name__)

# Set up logging to capture all output including print statements
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

SESSIONS: dict[str, session.Session] = {}


@app.route("/create_session")
def create_session():
    i = 0
    while f"session_{i}" in SESSIONS:
        i += 1

    SESSIONS[f"session_{i}"] = session.create_session()

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
    app.run(debug=True, port=5000, host="0.0.0.0")
