import os
import requests
import pyttsx3

from speech.stt import listen
from ai.brain import ask_ai


# =========================
# FLASK API
# =========================

API_URL = "http://127.0.0.1:5000/api"


def send_interaction(language, question, answer):
    try:
        response = requests.post(
            f"{API_URL}/interactions",
            json={
                "language": language,
                "question": question,
                "answer": answer
            },
            timeout=5
        )

        response.raise_for_status()

        print("📊 Interaction envoyée au dashboard.")

    except requests.RequestException as e:
        print("⚠️ Dashboard indisponible :", e)


# =========================
# TTS
# =========================

engine = pyttsx3.init()


def speak(text):
    print("🔊 TTS :", text)

    output_file = os.path.abspath("audio/response.wav")

    engine.save_to_file(text, output_file)
    engine.runAndWait()

    print("🔊 Audio saved :", output_file)

    os.startfile(output_file)


# =========================
# ASSISTANT
# =========================

print("🤖 Assistant démarré !")

while True:

    # 🎤 Speech-to-Text
    text, language = listen()

    if text is None:
        continue

    print("📝 Texte reconnu :", text)
    print("🌍 Langue :", language)

    # =========================
    # STOP COMMAND
    # =========================

    stop_commands = [
        "quitte",
        "quitter",
        "arrête",
        "arrêter",
        "au revoir",
        "exit",
        "quit",
        "stop"
    ]

    if text.lower().strip() in stop_commands:

        print("👋 Au revoir !")

        if language == "en":
            goodbye = "Goodbye!"
        else:
            goodbye = "Au revoir !"

        speak(goodbye)

        send_interaction(
            language,
            text,
            goodbye
        )

        break

    # =========================
    # AI RESPONSE
    # =========================

    try:

        answer = ask_ai(text, language)

        if answer is None:
            continue

        print("🤖 Assistant :", answer)

        # 🔊 Text-to-Speech
        speak(answer)

        # 📊 Send real interaction to dashboard
        send_interaction(
            language,
            text,
            answer
        )

    except Exception as e:

        print("❌ Erreur :", e)

        if language == "en":
            error_message = (
                "Sorry, something went wrong. "
                "Please try again."
            )
        else:
            error_message = (
                "Désolé, une erreur est survenue. "
                "Veuillez réessayer."
            )

        speak(error_message)

        send_interaction(
            language,
            text,
            error_message
        )