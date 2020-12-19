#!/bin/bash
echo -e 'power on \nagent on\ndiscoverable on \npairable on \nquit' | bluetoothctl
python3.7 /home/pi/SmartGrove/Raspberry/Cliente.py &


