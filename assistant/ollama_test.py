import requests
url = "http://localhost:11434/api/generate"

data = {
    "model": "qwen2.5:3b",
    "prompt": "Bonjour, comment allez-vous ?",
    "stream": False
}

response = requests.post(url, json=data)

result = response.json()

print("Réponse :", result["response"])