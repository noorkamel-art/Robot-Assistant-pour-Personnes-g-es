import requests
from datetime import datetime


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"


def clean_answer(answer):
    """
    Remove Qwen's internal thinking/reasoning from the response.
    """

    if "<think>" in answer and "</think>" in answer:
        answer = answer.split("</think>", 1)[1]

    answer = answer.replace("<think>", "")
    answer = answer.replace("</think>", "")

    return answer.strip()


def ask_ai(prompt, language):

    now = datetime.now().strftime("%H:%M")

    # =========================
    # RESPONSE LANGUAGE
    # =========================

    if language == "fr":
        response_language = "French"

    elif language == "en":
        response_language = "English"

    else:
        response_language = "the same language used by the user"

    # =========================
    # SYSTEM INSTRUCTIONS
    # =========================

    system_prompt = f"""
You are an intelligent multilingual voice assistant
inside an assistance robot.

Your job is to understand the complete meaning of the
user's message and answer it correctly.

The user can ask ANY kind of question.

Do not use keyword matching.
Do not classify the user's question based on isolated words.
Understand the complete sentence and its meaning.

SUPPORTED LANGUAGES:
- French
- English

CURRENT USER LANGUAGE:
{response_language}

LANGUAGE RULE:

The answer MUST be entirely in the same language
as the user's current message.

French input -> French answer.
English input -> English answer.

Never switch languages.

Do not translate the user's question unless requested.

If the question is unclear, ask for clarification
in the same language.

Do not invent information.

CURRENT SYSTEM TIME:
{now}

If the user asks for the current time, use this exact time:
{now}

VOICE RESPONSE:

The answer will be spoken aloud.

Give a concise, natural answer.
Do not produce long explanations unless the user asks
for a detailed explanation.

Return ONLY the final answer.
Do not include analysis.
Do not include reasoning.
Do not include a "thinking" section.
Do not include <think> tags.
"""

    # =========================
    # SEND TO OLLAMA
    # =========================

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "think": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data["message"]["content"].strip()

        # =========================
        # REMOVE THINKING
        # =========================

        answer = clean_answer(answer)

        if not answer:
            print("❌ Empty AI response")
            return None

        return answer

    except requests.RequestException as e:

        print("❌ Erreur Ollama :", e)
        return None


# =========================
# MANUAL TEST
# =========================

if __name__ == "__main__":

    while True:

        question = input("You: ")

        if question.lower().strip() in ["quit", "exit"]:
            break

        print("\nChoose language:")
        print("fr = French")
        print("en = English")

        language = input("Language: ").strip().lower()

        if language not in ["fr", "en"]:
            print("❌ Unsupported language")
            continue

        answer = ask_ai(question, language)

        if answer:
            print("🤖 Assistant:", answer)