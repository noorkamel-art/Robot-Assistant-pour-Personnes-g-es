import pyttsx3

engine = pyttsx3.init()

text = "Hello, I am your assistant. How can I help you today?"

engine.say(text)
engine.runAndWait()