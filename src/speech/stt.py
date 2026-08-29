import sounddevice as sd
import soundfile as sf
import speech_recognition as sr


recognizer = sr.Recognizer()


def listen():
    print("🎤 Parlez maintenant...")

    sample_rate = 16000
    duration = 10

    print("👂 J'écoute...")

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
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language="fr-FR"
        )

        print("📝 Texte reconnu :", text)
        return text

    except sr.UnknownValueError:
        print("❌ Je n'ai pas compris.")
        return None

    except sr.RequestError as e:
        print("❌ Erreur du service STT :", e)
        return None