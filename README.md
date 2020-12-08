# Smart Grove Project
This project have done to EI1057 - Networks and Mobile Devices subject.

## Objective

The objetive of this project are create mobile phone aplication for android and we use ESP32 with LoRa to monitor the whole crop.

## How it works?

All ESP32 have connected using ESP32 LoRa Wan networks, then, mobile phone have connected to ESP32 node using bluetooth. Also, phone upload data in excel google drive when it connects to esp32 main node.

## Matherials

* Raspberry Pi with Raspbian SO.
* ESP32 TTGO with Lora, Wifi and bluetooth.
* Google Drive library for excel

## Rapsberry configuring

We used Raspbian SO and we have confiured SSH server on Raspberry.

### Bluetoth server

1. Install bluetooth packages:

```
sudo apt update
sudo apt install bluetooth
sudo apt install bluez
sudo apt install python-bluez
sudo apt install bluez-utils
```
2. The we pair ESP32 device
```
sudo bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# discoverable on
[bluetooth]# pairable on
[bluetooth]# scan on
[bluetooth]# pair <mac>
[bluetooth]# paired-devices
```

3. Set the port
```
sudo sdptool add --channel=22 SP
sudo sdptool browse local
```
If it gives an error we must configure the file /lib/systemd/system/bluetooth.service and we have to add -compat option as this:

```
ExecStart=/usr/lib/bluetooth/bluetoothd --compat
```
Then we execute:
```
sudo systemctl daemon-reload
sudo systemctl restart bluetooth

sudo chmod 777 /var/run/sdp
sudo sdptool add --channel=22 SP
```

## Configuring Arduino IDE for ESP32

We follow [this tutorial](https://randomnerdtutorials.com/ttgo-lora32-sx1276-arduino-ide/) and it is working.

We are use TTGO LoRa32-OLED V1.

## Authors

This project are made by [Joaquín Gonlález](https://www.linkedin.com/in/joaquin-gonzalez-alvarez-52b234114/) and [Jose  Carlos Torró](https://www.linkedin.com/in/jose-carlos-torr%C3%B3-a94b67194/) 

