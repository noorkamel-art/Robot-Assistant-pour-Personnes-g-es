import asyncio
import os
import pygame
import edge_tts


async def generate_audio(text, filename):
    communicate = edge_tts.Communicate(
        text,
        "fr-FR-DeniseNeural"
    )
    await communicate.save(filename)


def speak(text):
    filename = "response.mp3"

    print("Génération de la voix...")

    asyncio.run(generate_audio(text, filename))

    print("Audio généré.")
    print("Lecture...")

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    os.remove(filename)

    print("Terminé.")

