import pyttsx3

engine = pyttsx3.init()

text = "Bonjour, comment allez-vous aujourd'hui ?"

engine.save_to_file(text, "audio/response.wav")
engine.runAndWait()

print("Audio generated: response.wav")