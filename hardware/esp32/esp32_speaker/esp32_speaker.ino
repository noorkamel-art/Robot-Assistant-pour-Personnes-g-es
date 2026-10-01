#include <Arduino.h>
#include "driver/i2s.h"
#include <math.h>

#define I2S_DOUT 22
#define I2S_BCLK 26
#define I2S_LRC  25

#define I2S_PORT I2S_NUM_0

#define SAMPLE_RATE 16000

void setupI2S() {

  i2s_config_t i2s_config = {

    .mode = (i2s_mode_t)(
      I2S_MODE_MASTER |
      I2S_MODE_TX
    ),

    .sample_rate = SAMPLE_RATE,

    .bits_per_sample =
      I2S_BITS_PER_SAMPLE_16BIT,

    .channel_format =
      I2S_CHANNEL_FMT_ONLY_LEFT,

    .communication_format =
      I2S_COMM_FORMAT_STAND_I2S,

    .intr_alloc_flags =
      ESP_INTR_FLAG_LEVEL1,

    .dma_buf_count = 8,
    .dma_buf_len = 64,

    .use_apll = false,

    .tx_desc_auto_clear = true,

    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {

    .bck_io_num = I2S_BCLK,

    .ws_io_num = I2S_LRC,

    .data_out_num = I2S_DOUT,

    .data_in_num =
      I2S_PIN_NO_CHANGE
  };

  i2s_driver_install(
    I2S_PORT,
    &i2s_config,
    0,
    NULL
  );

  i2s_set_pin(
    I2S_PORT,
    &pin_config
  );

  i2s_zero_dma_buffer(I2S_PORT);
}

void playTone(
  int frequency,
  int duration
) {

  const int samples =
    SAMPLE_RATE / 100;

  int16_t buffer[samples];

  unsigned long start = millis();

  while (
    millis() - start <
    duration
  ) {

    for (
      int i = 0;
      i < samples;
      i++
    ) {

      float value =
        sin(
          2.0 *
          PI *
          frequency *
          i /
          SAMPLE_RATE
        );

      buffer[i] =
        (int16_t)(
          value * 12000
        );
    }

    size_t bytes_written;

    i2s_write(
      I2S_PORT,
      buffer,
      sizeof(buffer),
      &bytes_written,
      portMAX_DELAY
    );
  }
}

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println("==============================");
  Serial.println(" ESP32 SPEAKER TEST");
  Serial.println("==============================");

  Serial.println();
  Serial.println("Initialisation MAX98357A...");

  setupI2S();

  Serial.println("✅ MAX98357A prêt");

  Serial.println();
  Serial.println("🔊 Test 440 Hz");

  playTone(440, 1000);

  delay(500);

  Serial.println("🔊 Test 880 Hz");

  playTone(880, 1000);

  Serial.println();
  Serial.println("✅ Test terminé");
}

void loop() {

  delay(2000);
}