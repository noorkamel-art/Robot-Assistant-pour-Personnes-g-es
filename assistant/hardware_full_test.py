import asyncio
import websockets
import wave
import requests
import edge_tts
import stt

HOST = "0.0.0.0"
PORT = 8765

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2

RECORD_SECONDS = 5
TARGET_BYTES = SAMPLE_RATE * SAMPLE_WIDTH * RECORD_SECONDS

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

TTS_FILE = "response_audio.raw"

VOICE = "fr-FR-DeniseNeural"

test_in_progress = False


# ==========================================
# OLLAMA
# ==========================================

def ask_ollama(question):

    print()
    print("🤖 Envoi vers Ollama...")

    data = {
        "model": MODEL,
        "prompt": question,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]


# ==========================================
# SAVE MICROPHONE AUDIO
# ==========================================

def save_wav(audio_data):

    filename = "test_audio.wav"

    with wave.open(filename, "wb") as wav:

        wav.setnchannels(CHANNELS)
        wav.setsampwidth(SAMPLE_WIDTH)
        wav.setframerate(SAMPLE_RATE)

        wav.writeframes(audio_data)

    print()
    print("✅ Fichier créé :", filename)
    print("📦 Taille :", len(audio_data), "bytes")
    print(
        f"⏱️ Durée : "
        f"{len(audio_data) / (SAMPLE_RATE * SAMPLE_WIDTH):.2f} secondes"
    )

    return filename


# ==========================================
# TTS
# ==========================================

async def generate_tts(text):

    print()
    print("🔊 Génération TTS...")

    communicate = edge_tts.Communicate(
        text,
        VOICE,
        output_format="raw-16khz-16bit-mono-pcm"
    )

    with open(TTS_FILE, "wb") as file:

        async for chunk in communicate.stream():

            if chunk["type"] == "audio":
                file.write(chunk["data"])

    print("✅ TTS terminé.")

    return TTS_FILE


# ==========================================
# SEND AUDIO TO ESP32
# ==========================================

async def send_audio_to_esp32(websocket, filename):

    print()
    print("🔊 Envoi de la réponse vers ESP32...")

    with open(filename, "rb") as file:

        while True:

            data = file.read(1024)

            if not data:
                break

            await websocket.send(data)

            # 1024 bytes
            # 2 bytes/sample
            # 16000 samples/sec

            await asyncio.sleep(
                1024 / (2 * SAMPLE_RATE)
            )

    await websocket.send("PLAYBACK_DONE")

    print("✅ Réponse envoyée au ESP32.")


# ==========================================
# ESP32 CONNECTION
# ==========================================

async def handle_client(websocket):

    global test_in_progress

    if test_in_progress:

        print("⚠️ Une session est déjà en cours.")

        await websocket.close()

        return

    test_in_progress = True

    print()
    print("================================")
    print("✅ ESP32 CONNECTÉ")
    print("================================")
    print()

    audio_data = bytearray()

    print("🎤 Parlez maintenant...")
    print(
        f"⏱️ Enregistrement "
        f"{RECORD_SECONDS} secondes"
    )

    try:

        async for message in websocket:

            # ==================================
            # ESP32 → PC
            # MICROPHONE
            # ==================================

            if isinstance(message, bytes):

                audio_data.extend(message)

                duration = (
                    len(audio_data)
                    / (SAMPLE_RATE * SAMPLE_WIDTH)
                )

                print(
                    f"\r🎤 {duration:.2f} / "
                    f"{RECORD_SECONDS} secondes",
                    end=""
                )

                # ==================================
                # RECORDING COMPLETE
                # ==================================

                if len(audio_data) >= TARGET_BYTES:

                    audio_data = audio_data[:TARGET_BYTES]

                    print()
                    print()
                    print("⏹️ Enregistrement terminé.")

                    filename = save_wav(
                        audio_data
                    )

                    # Tell ESP32 to stop microphone
                    await websocket.send(
                        "RECORDING_DONE"
                    )

                    # ==================================
                    # STT
                    # ==================================

                    print()
                    print("🎤 STT...")

                    question = stt.recognize_file(
                        filename
                    )

                    if not question:

                        print(
                            "❌ Aucun texte reconnu."
                        )

                        break

                    print()
                    print("================================")
                    print("📝 QUESTION")
                    print("================================")
                    print(question)
                    print("================================")

                    # ==================================
                    # OLLAMA
                    # ==================================

                    try:

                        response = ask_ollama(
                            question
                        )

                    except Exception as error:

                        print()
                        print(
                            "❌ Erreur Ollama :",
                            error
                        )

                        break

                    print()
                    print("================================")
                    print("🤖 RÉPONSE OLLAMA")
                    print("================================")
                    print(response)
                    print("================================")

                    # ==================================
                    # TTS
                    # ==================================

                    try:

                        tts_file = await generate_tts(
                            response
                        )

                    except Exception as error:

                        print()
                        print(
                            "❌ Erreur TTS :",
                            error
                        )

                        break

                    # ==================================
                    # ESP32 → MAX98357A → SPEAKER
                    # ==================================

                    try:

                        await send_audio_to_esp32(
                            websocket,
                            tts_file
                        )

                    except Exception as error:

                        print()
                        print(
                            "❌ Erreur Speaker :",
                            error
                        )

                        break

                    print()
                    print("================================")
                    print("🎉 FULL PIPELINE TERMINÉE")
                    print("================================")
                    print()
                    print(
                        "INMP441"
                        " → ESP32"
                        " → WebSocket"
                        " → STT"
                        " → Ollama"
                        " → TTS"
                        " → ESP32"
                        " → MAX98357A"
                        " → Speaker"
                    )
                    print()

                    break

    except websockets.exceptions.ConnectionClosed:

        print()
        print("❌ ESP32 déconnecté.")

    except Exception as error:

        print()
        print("❌ Erreur serveur :", error)

    finally:

        test_in_progress = False

        print()
        print("⏸️ Session terminée.")
        print("En attente de ESP32...")
        print()


# ==========================================
# SERVER
# ==========================================

async def main():

    print()
    print("================================")
    print(" ESP32 FULL HARDWARE TEST")
    print("================================")
    print()

    print("Pipeline :")
    print()
    print("🎤 INMP441")
    print("↓")
    print("ESP32")
    print("↓")
    print("WebSocket")
    print("↓")
    print("STT")
    print("↓")
    print("Ollama / Qwen")
    print("↓")
    print("TTS")
    print("↓")
    print("ESP32")
    print("↓")
    print("MAX98357A")
    print("↓")
    print("🔊 Speaker")
    print()

    print(
        f"Serveur : {HOST}:{PORT}"
    )

    print()
    print("En attente de ESP32...")
    print()

    async with websockets.serve(
        handle_client,
        HOST,
        PORT
    ):

        await asyncio.Future()


if __name__ == "__main__":

    asyncio.run(main())