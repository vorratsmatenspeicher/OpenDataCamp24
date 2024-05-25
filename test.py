from pathlib import Path

import openai

import session

import dotenv

dotenv.load_dotenv()


data_agent = session.DataAgent()

SYSTEM_PROMPT = f"""
Verhalte dich wie ein Berater zum Thema Bewältigung und Umgang mit Hitze. Gib konkrete Handlungsempfehlungen auf Anfragen. Nutze folgende APIs, um deine Anfragen mit spezifischen Daten zu füllen.
Um eine API auszuführen, antworte NUR mit dem Namen der API sowie den Argumenten in JSON-Form. Beende danach deine Antwort. Frage keine APIs, an wenn der Benutzer nicht nach relevaten Informationen gefragt hat. Folgende APIs stehen dir zur Verfügung:
{data_agent.get_services_description()}
Es folgen Beispiele für die API-Aufrufe:
"""

dialog_agent = session.OpenAiDialogAgent(
    openai_client=openai.Client(),
    messages=[
        session.Message(
            role="system",
            content=SYSTEM_PROMPT
        ),
        session.Message(
            role="system",
            content='{"service": "CLOCK", args: {}}'
        ),
        session.Message(
            role="system",
            content=str(data_agent.invoke_service("CLOCK", {}))
        )
    ]
)

session = session.Session(data_agent, dialog_agent)


while 1:
    prompt = input(" --> ")
    session.get_response(prompt)
