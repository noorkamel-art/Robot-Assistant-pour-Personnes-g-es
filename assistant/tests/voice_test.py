import speech_recognition as sr
import edge_tts
import pygame
import asyncio
import os

recognizer = sr.Recognizer()

pygame.mixer.init()


async def generate_audio(text, filename):
    communicate = edge_tts.Communicate(
        text,
        "fr-FR-DeniseNeural"
    )
    await communicate.save(filename)


def speak(text):
    filename = "response.mp3"

    asyncio.run(generate_audio(text, filename))

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(filename)


print("Assistant vocal demarre.")
print("Dites 'quitter' pour arreter le programme.")


while True:

    with sr.Microphone() as source:
        print("\nParlez maintenant...")
        audio = recognizer.listen(source)

    print("Reconnaissance de votre voix...")

    try:
        question = recognizer.recognize_google(
            audio,
            language="fr-FR"
        )

        print("Question :", question)

        question_clean = question.lower()

        if "quitter" in question_clean:
            response = "Au revoir !"

        elif "bonjour" in question_clean:
            response = "Bonjour, comment allez-vous ?"

        elif "ça va" in question_clean or "ca va" in question_clean:
            response = "Je vais bien, merci."

        elif "merci" in question_clean:
            response = "Avec plaisir."

        else:
            response = "Je suis désolé, je ne connais pas encore la réponse."

        print("Réponse :", response)

        speak(response)

        if "quitter" in question_clean:
            break

    except sr.UnknownValueError:
        print("Je n'ai pas compris votre voix.")

    except sr.RequestError as e:
        print("Erreur du service de reconnaissance vocale :", e)