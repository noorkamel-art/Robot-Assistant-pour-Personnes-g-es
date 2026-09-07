import pyttsx3

engine = pyttsx3.init()

text = "Hello, I am your assistant. How can I help you today?"

engine.save_to_file(text, "assistant/audio/response.wav")
engine.runAndWait()

print("Audio saved successfully.")