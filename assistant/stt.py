import speech_recognition as sr


recognizer = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        audio = recognizer.listen(source)

    print("Reconnaissance de votre voix...")
    try:
        text = recognizer.recognize_google(
        audio,
        language="fr-FR"
    )

        return text
    except sr.UnknownValueError:
        print("je n'ai pas compris.")
        return("")
    except sr.RequestError:
        print("Erreur du service de reconnaissance vocale.")
        return ""