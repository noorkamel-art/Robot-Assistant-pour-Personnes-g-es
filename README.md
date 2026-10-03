# Robot Assistant pour Personnes Âgées

Projet de développement d'un robot assistant intelligent destiné aux personnes âgées vivant seules.

## Architecture

Le système est basé sur :

- ESP32
- Microphone INMP441
- Amplificateur MAX98357A
- Haut-parleur 4Ω / 3W
- Écran TFT ST7735S 1.8" 128x160
- Capteur de fréquence cardiaque MAX30102
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

Capteurs et interface robot
      ↓
ESP32
      ├── TFT ST7735S
      └── MAX30102

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
TFT ST7735S
- Écran TFT LCD 1.8"
- Résolution : 128x160
- Interface SPI
- Affichage des yeux du robot
- Affichage de la fréquence cardiaque
- Communication avec l'ESP32
MAX30102
- Capteur de fréquence cardiaque
- Communication I2C
- Mesure du BPM
- Intégré avec l'affichage TFT
- Adresse I2C : 0x57
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
- TFT ST7735S testé
- MAX30102 testé
- Intégration TFT + MAX30102 fonctionnelle
- Affichage des yeux du robot fonctionnel
- Affichage du BPM fonctionnel
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
│   ├── dashboard/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   │
│   └── hardware/
│       └── esp32/
│           ├── esp32_microphone/
│           ├── esp32_speaker/
│           ├── esp32_full_audio/
│           └── esp32_tft_max30102/
│
├── hardware/
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
- SPI
- I2C
- TFT ST7735S
- MAX30102
- HTML
- CSS
- JavaScript
Prochaines étapes
Le projet continuera avec l'intégration progressive des différents composants matériels afin de construire un prototype complet du robot assistant.
Les prochaines étapes concernent notamment :
- l'intégration physique des composants dans le prototype
- l'amélioration de l'interface graphique du robot
- l'intégration progressive des fonctions vocales et des capteurs
- les tests fonctionnels finaux
- la préparation du prototype pour la démonstration