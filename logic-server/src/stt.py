import speech_recognition as sr

def main():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Capture the audio from the microphone
    with sr.Microphone() as source:
        print("Please say something:")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
        except sr.RequestError:
            print("Could not request results from Google Web Speech API")

if __name__ == "__main__":
    main()
