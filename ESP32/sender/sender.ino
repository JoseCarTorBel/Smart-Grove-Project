
//Libraries for LoRa
#include <SPI.h>
#include <LoRa.h>

#include <SimpleDHT.h>
int pinDHT11 = 16;
SimpleDHT11 dht11;
//

//Libraries for OLED Display
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

//define the pins used by the LoRa transceiver module
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26

//433E6 for Asia
//866E6 for Europe
//915E6 for North America
#define BAND 866E6

//OLED pins
#define OLED_SDA 4
#define OLED_SCL 15 
#define OLED_RST 16
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

//packet counter
int counter = 0;
int temperaturaAnterior, humedadAnterior;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RST);

void setup() {

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
  display.print("LORA SENDER ");
  display.display();
  
  //initialize Serial Monitor
  Serial.begin(115200);
  
  Serial.println("LoRa Sender Test");

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
  display.print("LoRa Initializing OK!");
  display.display();
  delay(2000);
}

void loop() {
  
 // read with raw sample datos.
  byte temperature = 0;
  byte humidity = 0;
  byte datas[40] = {0};
//
  display.clearDisplay();
   display.setCursor(0,0);
   display.println("Esto no va");
   display.display();
   
    delay(1000);
  
  if (dht11.read(pinDHT11, &temperature, &humidity, datas)) {
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("Read DHT11 failed");
    display.display();
    return;
  }

  if( (temperaturaAnterior!= NULL && humedadAnterior!= NULL) || 
      (temperaturaAnterior!= temperature && humedadAnterior!= humidity))
      {
        //dht11.read(pinDHT11, &temperature, &humidity, datas);
        display.clearDisplay();
        display.setCursor(0,0);
        display.println("LORA SENDER");
        display.setCursor(0,20);
        display.setTextSize(1);
        display.print((int)temperature); display.print("*C, ");
          
        display.setCursor(0,30);
        display.print((int)humidity); display.println(" %");
        display.display();

        temperaturaAnterior =  temperature;
        humedadAnterior = humidity;
        
        // LoRa Send packet
        LoRa.beginPacket();
        LoRa.print(temperature);
        LoRa.print("#");
        LoRa.print(humidity);
        LoRa.endPacket();

         counter++;
      }  
  delay(1000);
}
