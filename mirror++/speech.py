import time
import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()


def pollAudio():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print(recognizer.recognize_sphinx(audio))
        return recognizer.recognize_sphinx(audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return None
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        return None
