import speech_recognition as sr
import subprocess
import pyttsx3

# =========================
# 1. STT - Audio to Text
# =========================

recognizer = sr.Recognizer()

audio_file = "assistant/audio/question.wav"

with sr.AudioFile(audio_file) as source:
    audio = recognizer.record(source)

try:
    question = recognizer.recognize_google(audio, language="fr-FR")
    print("Texte reconnu :", question)

except sr.UnknownValueError:
    print("Impossible de comprendre l'audio.")
    exit()

except sr.RequestError as e:
    print("Erreur du service STT :", e)
    exit()


# =========================
# 2. LLM - Text to Response
# =========================

result = subprocess.run(
    ["ollama", "run", "qwen2.5:3b", question],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

response = result.stdout.strip()

print("Réponse de Qwen :")
print(response)


# =========================
# 3. TTS - Response to Audio
# =========================

engine = pyttsx3.init()

engine.save_to_file(
    response,
    "assistant/audio/response.wav"
)

engine.runAndWait()

print("Response audio saved successfully.")