import speech_recognition as sr


recognizer = sr.Recognizer()


# ==================================================
# STT depuis microphone PC
# ==================================================

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

        print("Je n'ai pas compris.")

        return ""

    except sr.RequestError:

        print("Erreur du service de reconnaissance vocale.")

        return ""


# ==================================================
# STT depuis fichier WAV
# ==================================================

def recognize_file(filename):

    print()
    print("🎤 Analyse du fichier audio...")
    print("📁 Fichier :", filename)

    try:

        with sr.AudioFile(filename) as source:

            audio = recognizer.record(source)


        print("🧠 Reconnaissance de votre voix...")

        text = recognizer.recognize_google(
            audio,
            language="fr-FR"
        )

        print()
        print("================================")
        print("📝 TEXTE RECONNU")
        print("================================")
        print(text)
        print("================================")
        print()

        return text


    except sr.UnknownValueError:

        print()
        print("❌ Je n'ai pas compris la voix.")
        print()

        return ""


    except sr.RequestError:

        print()
        print("❌ Erreur du service de reconnaissance vocale.")
        print()

        return ""


    except Exception as error:

        print()
        print("❌ Erreur STT :", error)
        print()

        return ""