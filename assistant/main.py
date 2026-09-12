import requests
import stt
import tts
from database import save_conversation, save_daily_activity
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

PATIENT_ID = 1


def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M")


def ask_ollama(question):
    data = {
        "model": MODEL,
        "prompt": question,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data
    )

    result = response.json()

    return result["response"]


print("Assistant vocal démarré.")
print("Dites 'quitter' pour arrêter.")


while True:

    # 1. Écouter la voix
    question = stt.listen()

    if not question:
        continue

    print("Question :", question)

    # 2. Arrêter si l'utilisateur dit quitter
    if "quitter" in question.lower():
        print("Au revoir !")
        break

    # 3. Vérifier si la question concerne l'heure
    question_lower = question.lower()

    if "heure" in question_lower or "temps" in question_lower:
        current_time = get_current_time()
        response = f"Il est actuellement {current_time}."

    else:
        # Envoyer la question à Ollama
        response = ask_ollama(question)

    # 4. Afficher la réponse
    print("Réponse :", response)

    # 5. Lire la réponse avec la voix
    tts.speak(response)

    # 6. Sauvegarder la conversation
    save_conversation(
        PATIENT_ID,
        question,
        response
    )

    # 7. Mettre à jour l'activité quotidienne
    save_daily_activity(PATIENT_ID)