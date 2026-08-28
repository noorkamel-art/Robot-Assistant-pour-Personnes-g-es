import asyncio
import edge_tts
import pygame
import os


async def generate_audio(text, filename):
    communicate = edge_tts.Communicate(
        text,
        "fr-FR-DeniseNeural"
    )
    await communicate.save(filename)


messages = [
    "Bonjour, comment allez-vous ?",
    "Je vais bien, merci.",
    "Avec plaisir."
]


pygame.mixer.init()

for i, message in enumerate(messages):

    filename = f"response_{i}.mp3"

    print("Generation :", message)

    asyncio.run(generate_audio(message, filename))

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()

    os.remove(filename)

print("Test termine.")