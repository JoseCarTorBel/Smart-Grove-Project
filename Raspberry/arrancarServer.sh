#!/bin/bash
echo -e 'power on \nagent on\ndiscoverable on \npairableon \nquit' | bluetoothctl
python3.7 /home/pi/Desktop/EI1057/Smart-grove-introductory-project/Raspberry/BluetoothServer.py &


