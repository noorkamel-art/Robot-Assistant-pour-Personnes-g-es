# MAX98357A

I2S digital audio amplifier used to drive the robot speaker.

## Connection with ESP32

| MAX98357A | ESP32 |
|----------|-------|
| VIN | 3.3V |
| GND | GND |
| BCLK | GPIO 26 |
| LRC | GPIO 25 |
| DIN | GPIO 22 |

## Speaker Connection

| MAX98357A | Speaker |
|----------|---------|
| SPK+ | Speaker + |
| SPK- | Speaker - |

**Important:** SPK- must not be connected to GND.

## Audio Configuration

- Interface: I2S
- Sample rate: 16 kHz
- Audio format: 16-bit PCM

## Usage

The MAX98357A receives digital audio from the ESP32 through I2S and drives the connected speaker.

It is used for the voice output of the robot assistant.

## Status

The MAX98357A and speaker were individually tested successfully.

The complete simultaneous microphone/speaker integration remains experimental.