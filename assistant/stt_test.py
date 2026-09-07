import speech_recognition as sr

recognizer = sr.Recognizer()

audio_file = "assistant/audio/question.wav"

with sr.AudioFile(audio_file) as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio, language="fr-FR")
    print("Texte reconnu :", text)

except sr.UnknownValueError:
    print("Impossible de comprendre l'audio.")

except sr.RequestError as e:
    print("Erreur du service STT :", e)