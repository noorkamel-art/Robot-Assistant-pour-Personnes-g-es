#include <WiFi.h>
#include <WebSocketsClient.h>
#include "driver/i2s.h"

const char* ssid = "TON_WIFI";
const char* password = "TON_MOT_DE_PASSE";

const char* SERVER_IP = "10.71.201.65";
const int SERVER_PORT = 8765;
const char* SERVER_PATH = "/audio";

#define I2S_WS   25
#define I2S_SCK  26
#define I2S_SD   33
#define I2S_PORT I2S_NUM_0

#define SAMPLE_RATE 16000
#define SAMPLES_PER_PACKET 128

int32_t i2s_samples[SAMPLES_PER_PACKET];
int16_t audio_samples[SAMPLES_PER_PACKET];

WebSocketsClient webSocket;

bool recordingFinished = false;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {

  switch (type) {

    case WStype_DISCONNECTED:
      Serial.println("❌ WebSocket déconnecté");
      break;

    case WStype_CONNECTED:
      Serial.println();
      Serial.println("✅ WebSocket connecté !");
      Serial.println("🎤 Audio streaming...");
      break;

    case WStype_TEXT:

      Serial.print("Server : ");
      Serial.println((char*)payload);

      if (strcmp((char*)payload, "RECORDING_DONE") == 0) {

        Serial.println();
        Serial.println("⏹️ Enregistrement terminé.");
        Serial.println("🛑 Arrêt du streaming audio.");

        recordingFinished = true;
      }

      break;

    default:
      break;
  }
}

void setupI2S() {

  i2s_config_t i2s_config = {

    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),

    .sample_rate = SAMPLE_RATE,

    .bits_per_sample =
      I2S_BITS_PER_SAMPLE_32BIT,

    .channel_format =
      I2S_CHANNEL_FMT_ONLY_LEFT,

    .communication_format =
      I2S_COMM_FORMAT_STAND_I2S,

    .intr_alloc_flags =
      ESP_INTR_FLAG_LEVEL1,

    .dma_buf_count = 8,
    .dma_buf_len = 64,

    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {

    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,

    .data_out_num =
      I2S_PIN_NO_CHANGE,

    .data_in_num = I2S_SD
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

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println("================================");
  Serial.println(" ESP32 MICROPHONE TEST");
  Serial.println("================================");

  Serial.print("Connexion Wi-Fi");

  WiFi.begin(
    ssid,
    password
  );

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("✅ Wi-Fi connecté");

  Serial.print("ESP32 IP : ");
  Serial.println(WiFi.localIP());

  Serial.println();
  Serial.println("Initialisation INMP441...");

  setupI2S();

  Serial.println("✅ INMP441 prêt");

  Serial.println();
  Serial.println("Connexion WebSocket...");

  webSocket.begin(
    SERVER_IP,
    SERVER_PORT,
    SERVER_PATH
  );

  webSocket.onEvent(webSocketEvent);

  webSocket.setReconnectInterval(3000);
}

void loop() {

  webSocket.loop();

  if (WiFi.status() != WL_CONNECTED)
    return;

  if (recordingFinished) {

    delay(100);
    return;
  }

  size_t bytes_read = 0;

  i2s_read(
    I2S_PORT,
    (void*)i2s_samples,
    sizeof(i2s_samples),
    &bytes_read,
    portMAX_DELAY
  );

  int samples_read =
    bytes_read / sizeof(int32_t);

  for (
    int i = 0;
    i < samples_read;
    i++
  ) {

    audio_samples[i] =
      (int16_t)(
        i2s_samples[i] >> 14
      );
  }

  if (
    samples_read > 0 &&
    webSocket.isConnected()
  ) {

    webSocket.sendBIN(
      (uint8_t*)audio_samples,
      samples_read * sizeof(int16_t)
    );
  }
}