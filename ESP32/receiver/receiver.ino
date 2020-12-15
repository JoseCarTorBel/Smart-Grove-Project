/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/ttgo-lora32-sx1276-arduino-ide/
*********/

//Libraries for LoRa
#include <SPI.h>
#include <LoRa.h>


//Libraries for OLED Display
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// BluetoothSerial
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif



//define the pins used by the LoRa transceiver module
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26

//866E6 for Europe
#define BAND 866E6

//OLED pins
#define OLED_SDA 4
#define OLED_SCL 15 
#define OLED_RST 16
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels



Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RST);

String LoRaData;
BluetoothSerial SerialBT;
//String MAC_RAPS = "B8:27:EB:A6:38:58";

int rssiAnterior = 0;
using namespace std;

void setup() { 

  Serial.begin(115200);
  SerialBT.begin("ServerESP32"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");

  
  //reset OLED display via software
  pinMode(OLED_RST, OUTPUT);
  digitalWrite(OLED_RST, LOW);
  delay(20);
  digitalWrite(OLED_RST, HIGH);
  
  //initialize OLED
  Wire.begin(OLED_SDA, OLED_SCL);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3c, false, false)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.print("LORA RECEIVER ");
  display.setCursor(0,1);
  display.print("Bluetooth active");
  display.display();
  
  //initialize Serial Monitor
  Serial.begin(115200);

  Serial.println("LoRa Receiver Test");
  
  //SPI LoRa pins
  SPI.begin(SCK, MISO, MOSI, SS);
  //setup LoRa transceiver module
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  Serial.println("LoRa Initializing OK!");
  display.setCursor(0,10);
  display.println("LoRa Initializing OK!");
  display.display();  
}

void loop() {

  //try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    //received a packet
    Serial.println("Received packet ");

    //read packet
    while (LoRa.available()) {  
      LoRaData = LoRa.readString();
    }
       int rssi = LoRa.packetRssi();
       if(SerialBT.connected(1)){
         if(rssiAnterior != rssi)
         {
  //          SerialBT.write(temperature.toInt());
            SerialBT.println(LoRaData);
            rssiAnterior = rssi;
            delay(10000);
          }      
      }
  
    volatile char separador = '#';
    String temperature = LoRaData.substring(0, LoRaData.indexOf(separador));
    String humidity = LoRaData.substring(LoRaData.indexOf(separador)+1);

    Serial.println("");
    Serial.println(temperature); Serial.println(humidity);
    
    //print RSSI of packet
    Serial.print(" with RSSI ");    
    Serial.println(rssi);




   // Dsiplay information
   display.clearDisplay();
   display.setCursor(0,0);
   display.print("LORA RECEIVER");
   display.setCursor(0,20);
   display.print("Received packet:");
   display.setCursor(0,30);
   display.print("Temperature: ");display.print(temperature); display.print(" *C");
   display.setCursor(0,40);
   display.print("Humity: ");display.print(humidity); display.println(" %");
   display.setCursor(0,40);
   display.display();   
  }
}
