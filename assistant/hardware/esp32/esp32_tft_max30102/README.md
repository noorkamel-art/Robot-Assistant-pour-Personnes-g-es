# TFT ST7735S + MAX30102

Module de test et d'intégration de l'écran TFT ST7735S avec le capteur de fréquence cardiaque MAX30102 sur ESP32.

## Composants

### TFT ST7735S

- Écran TFT LCD 1.8"
- Résolution : 128x160
- Interface : SPI
- Contrôleur : ST7735S

### MAX30102

- Capteur de fréquence cardiaque
- Mesure du BPM
- Interface : I2C
- Adresse I2C : 0x57

## Connexions

### TFT ST7735S → ESP32

| TFT | ESP32 |
|---|---|
| GND | GND |
| VCC | 3.3V |
| SCL | GPIO18 |
| SDA | GPIO23 |
| RES | GPIO17 |
| DC | GPIO16 |
| CS | GPIO5 |
| BL | 3.3V |

### MAX30102 → ESP32

| MAX30102 | ESP32 |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO19 |
| INT | Non connecté |

## Fonctionnement

L'ESP32 utilise le TFT pour afficher l'interface graphique du robot.

L'écran affiche :

- les yeux du robot
- l'état de la mesure cardiaque
- la fréquence cardiaque en BPM

Le MAX30102 mesure le rythme cardiaque lorsqu'un doigt est placé sur le capteur.

Les données du capteur sont traitées par l'ESP32 puis affichées directement sur le TFT.

## Interface graphique

Le prototype utilise une animation simple des yeux :

- yeux ouverts
- yeux fermés
- clignement automatique

Lorsque le doigt est détecté sur le MAX30102, le BPM est affiché sur l'écran.

Lorsque aucun doigt n'est détecté, l'écran affiche une indication pour placer le doigt sur le capteur.

## Bibliothèques utilisées

```text
Adafruit GFX Library
Adafruit ST7735 and ST7789 Library
SparkFun MAX3010x Sensor Library

Code
Le programme principal se trouve dans :
esp32_tft_max30102.ino

Test réalisé
Le fonctionnement des deux composants a été testé avec l'ESP32.
Tests réalisés :
- Initialisation du TFT
- Affichage des couleurs
- Affichage des yeux du robot
- Initialisation du MAX30102
- Détection du doigt
- Mesure du BPM
- Affichage du BPM sur le TFT
- Fonctionnement simultané du TFT et du MAX30102
État
TFT + MAX30102 : fonctionnels et testés.