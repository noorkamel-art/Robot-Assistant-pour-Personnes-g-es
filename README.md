# Robot Assistant pour Personnes Âgées

Projet de développement d'un robot assistant intelligent destiné aux personnes âgées vivant seules.

## Architecture

Le système est basé sur :

- ESP32
- Microphone INMP441
- Amplificateur MAX98357A
- Haut-parleur 4Ω / 3W
- PC local pour le traitement
- Ollama + Qwen2.5:3b
- Speech-to-Text (STT)
- Text-to-Speech (TTS)
- Supabase
- Dashboard Web

## Fonctionnement

```text
Voix utilisateur
      ↓
STT
      ↓
Texte
      ↓
Ollama / Qwen2.5:3b
      ↓
Réponse texte
      ↓
TTS
      ↓
Réponse vocale

Les conversations et l'activité quotidienne sont enregistrées dans Supabase.
Base de données
Tables principales :
- patients
- conversations
- alerts
- activity
Le backend contient également la gestion des rappels.
Dashboard
Le dashboard Web permet de consulter :
- les informations du patient
- l'historique des conversations
- les alertes
- les rappels
- l'activité quotidienne
Le dashboard communique avec le backend Python via une API Flask.
Hardware
ESP32
- ESP32-WROOM-32 NodeMCU
INMP441
- Interface I2S
- Sample rate : 16 kHz
- Format : 32-bit I2S
- Conversion vers PCM 16-bit
MAX98357A
- Amplificateur audio I2S
- Haut-parleur 4Ω / 3W
- Sample rate : 16 kHz
- Format : PCM 16-bit
État actuel
Software
- Ollama installé et testé
- STT fonctionnel
- TTS fonctionnel
- Intégration STT + LLM + TTS
- Tests de fiabilité vocale
- Backend Flask
- Base de données Supabase
- Dashboard Web
- Système de rappels
Hardware
- ESP32 testé
- INMP441 testé individuellement
- MAX98357A testé individuellement
- Haut-parleur testé
- Intégration microphone + haut-parleur encore expérimentale

Robot-Assistant-pour-Personnes-g-es/
│
├── assistant/
│   ├── main.py
│   ├── api.py
│   ├── database.py
│   ├── stt.py
│   ├── tts.py
│   ├── hardware_full_test.py
│   ├── reminder_scheduler.py
│   │
│   └── dashboard/
│       ├── index.html
│       ├── script.js
│       └── style.css
│
├── hardware/
│   ├── esp32/
│   │   ├── esp32_microphone/
│   │   ├── esp32_speaker/
│   │   └── esp32_full_audio/
│   │
│   ├── inmp441/
│   │   └── README.md
│   │
│   └── max98357a/
│       └── README.md
│
├── requirements.txt
└── README.md

Technologies
- Python
- Flask
- SpeechRecognition
- Edge TTS
- Ollama
- Qwen2.5:3b
- Supabase
- PostgreSQL
- ESP32
- I2S
- HTML
- CSS
- JavaScript

Prochaines étapes
Le projet continuera avec l'intégration progressive de nouveaux composants matériels et l'amélioration de l'interaction entre le robot, le backend et le dashboard.