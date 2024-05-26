import typing

import dotenv
from openai import OpenAI

dotenv.load_dotenv()


def _retrieve_from_file(assistant_id, prompt):
    client = OpenAI()

    assistant = client.beta.assistants.retrieve(
        assistant_id=assistant_id if assistant_id else "asst_iwLP1f7aRgI9N3uD93TlojYA"
    )

    # Upload the user provided file to OpenAI
    # message_file = client.beta.vector_stores.retrieve(vector_store_id=vector_store_id if vector_store_id else "vs_pLpEAa2FTxQXX1Gkorw5RSJQ")

    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        model=assistant.model,
        stream=True
    )


def retrieve_from_file(assistant_id, prompt) -> typing.Generator[str, None, None]:
    for chunk in _retrieve_from_file(assistant_id, prompt):
        if chunk.event == "thread.message.delta":
            yield chunk.data.delta.content[0].text.value


# Beispiel zur Nutzung der Funktion
if __name__ == "__main__":
    for t in retrieve_from_file(None, "Warum sind Menschen ab 65 besonders von Hitze betroffen?"):
        print(t)
