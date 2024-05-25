import dotenv
from openai import OpenAI

dotenv.load_dotenv()

def retrieve_from_file(assistant_id, vector_store_id, prompt, streaming):
    client = OpenAI()
    
    assistant = client.beta.assistants.retrieve(
        assistant_id = assistant_id if assistant_id else "asst_iwLP1f7aRgI9N3uD93TlojYA"
    )

    # Upload the user provided file to OpenAI
    #message_file = client.beta.vector_stores.retrieve(vector_store_id=vector_store_id if vector_store_id else "vs_pLpEAa2FTxQXX1Gkorw5RSJQ")

    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
    )

    def run_without_streaming():
        # Use the create and poll SDK helper to create a run and poll the status of
        # the run until it's in a terminal state.

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))
        return message_content.value

    def run_with_streaming():
        from typing_extensions import override
        from openai import AssistantEventHandler
        
        # First, we create a EventHandler class to define
        # how we want to handle the events in the response stream.
        
        class EventHandler(AssistantEventHandler):    
            @override
            def on_text_created(self, text) -> None:
                print(f"\nassistant > ", end="", flush=True)
                
            @override
            def on_text_delta(self, delta, snapshot):
                print(delta.value, end="", flush=True)
                
            def on_tool_call_created(self, tool_call):
                print(f"\nassistant > {tool_call.type}\n", flush=True)
            
            def on_tool_call_delta(self, delta, snapshot):
                if delta.type == 'code_interpreter':
                    if delta.code_interpreter.input:
                        print(delta.code_interpreter.input, end="", flush=True)
                    if delta.code_interpreter.outputs:
                        print(f"\n\noutput >", flush=True)
                        for output in delta.code_interpreter.outputs:
                            if output.type == "logs":
                                print(f"\n{output.logs}", flush=True)
            
        # Then, we use the `stream` SDK helper 
        # with the `EventHandler` class to create the Run 
        # and stream the response.
        
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()

    if streaming: 
        run_with_streaming() 
    else: 
        return run_without_streaming()
    return None

# Beispiel zur Nutzung der Funktion
if __name__ == "__main__":
    retrieve_from_file(None, None, "Warum sind Menschen ab 65 besonders von Hitze betroffen?", True)