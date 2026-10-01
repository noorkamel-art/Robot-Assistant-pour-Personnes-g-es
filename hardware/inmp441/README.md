# INMP441

Digital I2S microphone used for voice input in the robot assistant project.

## Connection with ESP32

| INMP441 | ESP32 |
|--------|-------|
| VDD | 3.3V |
| GND | GND |
| SCK | GPIO 26 |
| WS | GPIO 25 |
| SD | GPIO 33 |
| L/R | GND |

## Audio Configuration

- Interface: I2S
- Sample rate: 16 kHz
- Microphone format: 32-bit I2S
- Converted audio format: 16-bit PCM

## Usage

The INMP441 captures the user's voice.

The ESP32 receives the digital audio through I2S and sends the audio stream to the local PC through WebSocket.

The PC then processes the audio using the speech-to-text pipeline.

## Status

The microphone was individually tested successfully.

The complete simultaneous microphone/speaker integration remains experimental.