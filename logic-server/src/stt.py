import threading
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize_speech(stop_event):
    # Load the German model
    https://alphacephei.com/vosk/models
    #model = Model("models/vosk-model-small-de-0.15")
    model = Model("../vosk-model-small-de-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    # Start the stream
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("Please say something in German and press Enter to stop listening:")

        while not stop_event.is_set():
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '')
                if text:
                    print("You said: " + text)

def wait_for_enter(stop_event):
    input()  # Wait for Enter key press
    stop_event.set()  # Signal to stop listening

if __name__ == "__main__":
    stop_event = threading.Event()

    # Start the listening thread
    listener_thread = threading.Thread(target=recognize_speech, args=(stop_event,))
    listener_thread.start()

    # Wait for the Enter key press
    wait_for_enter(stop_event)

    # Wait for the listener thread to finish
    listener_thread.join()

