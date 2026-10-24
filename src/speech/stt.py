import json
import os

import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel


# =========================
# WHISPER MODEL
# =========================

model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)


# =========================
# SAVE TRANSCRIPTION
# =========================

def save_transcription(text, language):
    os.makedirs("audio", exist_ok=True)

    # Save readable UTF-8 text
    with open("audio/transcription.txt", "w", encoding="utf-8") as file:
        file.write(text)

    # Save structured data
    data = {
        "language": language,
        "text": text
    }

    with open("audio/transcription.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# =========================
# SPEECH TO TEXT
# =========================

def listen():
    print("🎤 Parlez / Speak...")

    sample_rate = 16000
    duration = 10

    print("👂 J'écoute / Listening...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    filename = "audio/temp.wav"
    sf.write(filename, recording, sample_rate)

    try:
        # =========================
        # AUTOMATIC LANGUAGE DETECTION
        # =========================

        segments, info = model.transcribe(
            filename,
            beam_size=5,
            vad_filter=True
        )

        segments = list(segments)

        text = " ".join(
            segment.text for segment in segments
        ).strip()

        language = info.language

        # =========================
        # SUPPORTED LANGUAGES
        # =========================

        if language not in ["fr", "en"]:
            print("⚠️ Langue non supportée :", language)
            print("⚠️ Supported languages: French, English")

            return None, None

        # =========================
        # EMPTY RESULT
        # =========================

        if not text:
            print(
                "❌ Je n'ai pas compris / "
                "I didn't understand."
            )

            return None, None

        # =========================
        # RESULT
        # =========================

        print("🌍 Langue détectée :", language)
        print("📝 Texte reconnu :", text)

        save_transcription(text, language)

        return text, language

    except Exception as e:
        print("❌ Erreur STT :", e)
        return None, None


# =========================
# TEST
# =========================

if __name__ == "__main__":
    text, language = listen()