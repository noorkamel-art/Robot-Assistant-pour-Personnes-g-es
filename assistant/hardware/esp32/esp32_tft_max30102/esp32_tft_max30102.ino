#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

#define TFT_CS    5
#define TFT_DC    16
#define TFT_RST   17
#define TFT_MOSI  23
#define TFT_SCLK  18

#define I2C_SDA   21
#define I2C_SCL   19

Adafruit_ST7735 tft(
  TFT_CS,
  TFT_DC,
  TFT_MOSI,
  TFT_SCLK,
  TFT_RST
);

MAX30105 particleSensor;

float bpm = 0;
long lastBeat = 0;

bool eyesClosed = false;
unsigned long lastBlink = 0;
unsigned long blinkDuration = 150;
unsigned long nextBlink = 3000;

void drawEyes(bool closed)
{
  tft.fillRect(0, 0, 160, 70, ST77XX_BLACK);

  if (closed)
  {
    tft.drawLine(25, 35, 60, 35, ST77XX_WHITE);
    tft.drawLine(100, 35, 135, 35, ST77XX_WHITE);
  }
  else
  {
    tft.fillRoundRect(20, 15, 45, 40, 10, ST77XX_WHITE);
    tft.fillRoundRect(95, 15, 45, 40, 10, ST77XX_WHITE);

    tft.fillCircle(42, 35, 8, ST77XX_BLACK);
    tft.fillCircle(117, 35, 8, ST77XX_BLACK);
  }
}

void drawBPM()
{
  tft.fillRect(0, 75, 160, 85, ST77XX_BLACK);

  tft.setTextSize(1);
  tft.setTextColor(ST77XX_WHITE);

  tft.setCursor(45, 78);
  tft.print("HEART RATE");

  tft.setTextSize(2);

  if (bpm > 0)
  {
    tft.setTextColor(ST77XX_GREEN);
    tft.setCursor(25, 100);
    tft.print("BPM ");
    tft.print((int)bpm);
  }
  else
  {
    tft.setTextColor(ST77XX_YELLOW);

    tft.setCursor(20, 105);
    tft.print("PLACE");

    tft.setCursor(25, 130);
    tft.print("FINGER");
  }
}

void setup()
{
  Serial.begin(115200);
  delay(1000);

  Serial.println("==========================");
  Serial.println(" ROBOT HEART RATE TEST");
  Serial.println("==========================");

  tft.initR(INITR_BLACKTAB);
  tft.setRotation(1);
  tft.fillScreen(ST77XX_BLACK);

  drawEyes(false);
  drawBPM();

  Wire.begin(I2C_SDA, I2C_SCL);

  Serial.println("Initialisation MAX30102...");

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST))
  {
    Serial.println("MAX30102 NOT FOUND!");

    tft.fillScreen(ST77XX_BLACK);
    tft.setTextColor(ST77XX_RED);
    tft.setTextSize(1);
    tft.setCursor(20, 60);
    tft.println("MAX30102 ERROR");

    while (1);
  }

  Serial.println("MAX30102 OK");

  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x1F);
  particleSensor.setPulseAmplitudeGreen(0);
  particleSensor.setPulseAmplitudeIR(0x1F);

  Serial.println("Place your finger on MAX30102");
}

void loop()
{
  long irValue = particleSensor.getIR();

  if (irValue < 50000)
  {
    bpm = 0;

    Serial.println("No finger");

    drawEyes(false);
    drawBPM();

    delay(200);
    return;
  }

  if (checkForBeat(irValue))
  {
    long delta = millis() - lastBeat;
    lastBeat = millis();

    float currentBPM = 60.0 / (delta / 1000.0);

    if (currentBPM > 40 && currentBPM < 200)
    {
      bpm = currentBPM;

      Serial.print("BPM = ");
      Serial.println(bpm);

      drawBPM();
    }
  }

  unsigned long currentTime = millis();

  if (!eyesClosed &&
      currentTime - lastBlink > nextBlink)
  {
    eyesClosed = true;
    lastBlink = currentTime;

    drawEyes(true);
  }

  if (eyesClosed &&
      currentTime - lastBlink > blinkDuration)
  {
    eyesClosed = false;
    lastBlink = currentTime;

    nextBlink = random(2000, 5000);

    drawEyes(false);
  }

  delay(20);
}