import subprocess

question = "Bonjour, pouvez-vous m'aider ?"

result = subprocess.run(
    ["ollama", "run", "qwen2.5:3b", question],
    capture_output=True,
    text=True,
encoding="utf-8"
)

print("Réponse de Qwen :")
print(result.stdout)