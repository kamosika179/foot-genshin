#include <WiFi.h>
#include <Adafruit_MPU6050.h>
#include <Wire.h>

// WiFiの設定
const char* ssid = "kamosikadayo";
const char* password = "sikakamokamo?";

// ArduinoのIPアドレスを指定する
IPAddress ip(192, 168, 0, 179);  // 任意のIPアドレスにゃ
IPAddress gateway(192, 168, 0, 1);  // ゲートウェイのIPアドレスにゃ
IPAddress subnet(255, 255, 255, 0);  // サブネットマスクのIPアドレスにゃ
IPAddress dns(8, 8, 8, 8);  // DNSサーバのIPアドレスにゃ

// サーバのIPアドレスとポート番号
IPAddress serverIP(192, 168, 0, 13);  // Python側のIPアドレスにゃ
unsigned int serverPort = 17900;  // Python側と同じポート番号にゃ

WiFiClient client;

Adafruit_MPU6050 mpu;

void setup() {
  // シリアル通信を開始する
  Serial.begin(9600);

  // I2C設定
  Wire.begin(6,7);

  // MPU6050設定
  mpu = Adafruit_MPU6050();
  mpu.begin();

  // WiFiに接続する
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // クライアントとサーバを接続する
  if (!client.connect(serverIP, serverPort)) {
    Serial.println("Connection failed");
    return;
  }
  Serial.println("Connected to server");

  Serial.print("加速度");
}

void loop() {
  
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // 加速度を送る(X,Y,Z)
  client.print(String(a.acceleration.x)+","+String(a.acceleration.y)+","+String(a.acceleration.z));
 
  // データの送信間隔を設定する
  delay(100);
}
