#include <WiFi.h>
#include <WebSocketsClient.h>
#include "driver/i2s.h"

// ========================================
// Wi-Fi
// ========================================

const char* ssid = "TON_WIFI";
const char* password = "TON_MOT_DE_PASSE";

const char* SERVER_IP = "10.71.201.65";
const int SERVER_PORT = 8765;
const char* SERVER_PATH = "/audio";

// ========================================
// INMP441 - I2S RX
// ========================================

#define I2S_RX_PORT I2S_NUM_0

#define MIC_WS   25
#define MIC_SCK  26
#define MIC_SD   33

// ========================================
// MAX98357A - I2S TX
// ========================================

#define I2S_TX_PORT I2S_NUM_1

#define SPK_BCLK 26
#define SPK_LRC  25
#define SPK_DOUT 22

// ========================================
// Audio
// ========================================

#define SAMPLE_RATE 16000
#define SAMPLES_PER_PACKET 128

int32_t mic_samples[SAMPLES_PER_PACKET];
int16_t audio_samples[SAMPLES_PER_PACKET];

WebSocketsClient webSocket;

bool recordingFinished = false;
bool playingResponse = false;

// ========================================
// Microphone I2S
// ========================================

void setupMicrophoneI2S() {

  i2s_config_t config = {

    .mode = (i2s_mode_t)(
      I2S_MODE_MASTER |
      I2S_MODE_RX
    ),

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

  i2s_pin_config_t pins = {

    .bck_io_num = MIC_SCK,

    .ws_io_num = MIC_WS,

    .data_out_num =
      I2S_PIN_NO_CHANGE,

    .data_in_num = MIC_SD
  };

  i2s_driver_install(
    I2S_RX_PORT,
    &config,
    0,
    NULL
  );

  i2s_set_pin(
    I2S_RX_PORT,
    &pins
  );

  i2s_zero_dma_buffer(
    I2S_RX_PORT
  );
}

// ========================================
// Speaker I2S
// ========================================

void setupSpeakerI2S() {

  i2s_config_t config = {

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

  i2s_pin_config_t pins = {

    .bck_io_num = SPK_BCLK,

    .ws_io_num = SPK_LRC,

    .data_out_num = SPK_DOUT,

    .data_in_num =
      I2S_PIN_NO_CHANGE
  };

  i2s_driver_install(
    I2S_TX_PORT,
    &config,
    0,
    NULL
  );

  i2s_set_pin(
    I2S_TX_PORT,
    &pins
  );

  i2s_zero_dma_buffer(
    I2S_TX_PORT
  );
}

// ========================================
// WebSocket
// ========================================

void webSocketEvent(
  WStype_t type,
  uint8_t* payload,
  size_t length
) {

  switch (type) {

    case WStype_DISCONNECTED:

      Serial.println(
        "❌ WebSocket déconnecté"
      );

      break;


    case WStype_CONNECTED:

      Serial.println();
      Serial.println(
        "✅ WebSocket connecté !"
      );

      Serial.println(
        "🎤 Full Audio prêt."
      );

      break;


    case WStype_TEXT:

      Serial.print(
        "Server : "
      );

      Serial.println(
        (char*)payload
      );


      if (
        strcmp(
          (char*)payload,
          "RECORDING_DONE"
        ) == 0
      ) {

        recordingFinished = true;

        Serial.println(
          "⏹️ Enregistrement terminé."
        );
      }


      if (
        strcmp(
          (char*)payload,
          "PLAYBACK_DONE"
        ) == 0
      ) {

        playingResponse = false;

        recordingFinished = false;

        Serial.println(
          "🔊 Lecture terminée."
        );

        Serial.println(
          "🎤 Prêt pour une nouvelle question."
        );
      }

      break;


    case WStype_BIN:

      // Réception de l'audio TTS
      playingResponse = true;

      i2s_write(
        I2S_TX_PORT,
        payload,
        length,
        NULL,
        portMAX_DELAY
      );

      break;


    default:

      break;
  }
}

// ========================================
// Setup
// ========================================

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println(
    "================================"
  );

  Serial.println(
    " ESP32 FULL AUDIO TEST"
  );

  Serial.println(
    "================================"
  );


  // Wi-Fi

  Serial.print(
    "Connexion Wi-Fi"
  );

  WiFi.begin(
    ssid,
    password
  );

  while (
    WiFi.status() != WL_CONNECTED
  ) {

    delay(500);

    Serial.print(".");
  }

  Serial.println();

  Serial.println(
    "✅ Wi-Fi connecté"
  );

  Serial.print(
    "ESP32 IP : "
  );

  Serial.println(
    WiFi.localIP()
  );


  // Microphone

  Serial.println();

  Serial.println(
    "Initialisation INMP441..."
  );

  setupMicrophoneI2S();

  Serial.println(
    "✅ INMP441 prêt"
  );


  // Speaker

  Serial.println();

  Serial.println(
    "Initialisation MAX98357A..."
  );

  setupSpeakerI2S();

  Serial.println(
    "✅ MAX98357A prêt"
  );


  // WebSocket

  Serial.println();

  Serial.println(
    "Connexion WebSocket..."
  );

  webSocket.begin(
    SERVER_IP,
    SERVER_PORT,
    SERVER_PATH
  );

  webSocket.onEvent(
    webSocketEvent
  );

  webSocket.setReconnectInterval(
    3000
  );
}

// ========================================
// Loop
// ========================================

void loop() {

  webSocket.loop();


  if (
    WiFi.status() != WL_CONNECTED
  ) {

    return;
  }


  // إذا قاعدين نسمعوا الرد
  // ما نبداوش نبعثوا microphone

  if (playingResponse) {

    delay(1);

    return;
  }


  if (recordingFinished) {

    delay(10);

    return;
  }


  // قراءة microphone

  size_t bytes_read = 0;

  i2s_read(
    I2S_RX_PORT,
    (void*)mic_samples,
    sizeof(mic_samples),
    &bytes_read,
    portMAX_DELAY
  );


  int samples_read =
    bytes_read /
    sizeof(int32_t);


  // 32-bit → 16-bit

  for (
    int i = 0;
    i < samples_read;
    i++
  ) {

    audio_samples[i] =
      (int16_t)(
        mic_samples[i] >> 14
      );
  }


  // إرسال audio إلى PC

  if (
    samples_read > 0 &&
    webSocket.isConnected()
  ) {

    webSocket.sendBIN(
      (uint8_t*)audio_samples,
      samples_read *
      sizeof(int16_t)
    );
  }
}