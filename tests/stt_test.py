import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.AudioFile("audio/question.wav") as source:    audio = recognizer.record(source)

text = recognizer.recognize_google(audio, language="fr-FR")

print("Texte reconnu :", text)