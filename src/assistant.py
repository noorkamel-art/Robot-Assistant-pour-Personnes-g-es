
import os
import pyttsx3

from speech.stt import listen
from ai.brain import ask_ai


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
    text = listen()

    if text is None:
        continue

    print("📝 Texte reconnu :", text)

    text_lower = text.lower().strip()

    # =========================
    # STOP COMMAND
    # =========================

    if text_lower in [
        "quitte",
        "quitter",
        "arrête",
        "arrêter",
        "au revoir"
    ]:
        print("👋 Au revoir !")
        speak("Au revoir !")
        break

    # =========================
    # AI RESPONSE
    # =========================

    try:
        answer = ask_ai(text)

        print("🤖 Assistant :", answer)

        # 🔊 Text-to-Speech
        speak(answer)

    except Exception as e:
        print("❌ Erreur :", e)
        speak("Désolé, je rencontre un problème. Veuillez réessayer.")

