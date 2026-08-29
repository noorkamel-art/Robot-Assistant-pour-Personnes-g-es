import requests
from datetime import datetime


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


def ask_ai(prompt):
    now = datetime.now().strftime("%H:%M")

    system_context = f"""
Tu es un assistant vocal intelligent pour un robot d'assistance.

HEURE ACTUELLE DU SYSTÈME : {now}

RÈGLES IMPORTANTES :
1. Tu DOIS utiliser l'heure ci-dessus pour répondre à toute question demandant l'heure actuelle.
2. Ne dis JAMAIS que tu ne peux pas connaître l'heure actuelle.
3. Ne dis JAMAIS que tu n'as pas accès aux informations en temps réel.
4. L'heure {now} est fournie directement par le système et est fiable.
5. Réponds en français si l'utilisateur parle français.
6. Réponds directement et naturellement.
7. N'invente pas d'informations qui ne sont pas fournies.

Question de l'utilisateur :
{prompt}

Réponds maintenant à la question.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": system_context,
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()["response"].strip()


if __name__ == "__main__":
    question = input("You: ")
    answer = ask_ai(question)

    print("Assistant:", answer)