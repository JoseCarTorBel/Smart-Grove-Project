import socket
import subprocess
import logging
from datetime import datetime
import I2C_LCD_driver
import time

lcd=I2C_LCD_driver.lcd()
logging.basicConfig( level=logging.DEBUG, filename='/home/pi/SmartGrove/Raspberry/Cliente.log')

serverMACAddress = 'F0:08:D1:C8:DB:FE'

port = 1
size=1024
logging.info("=========================================================================")
while(1):
	try:
		s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

		logging.info("----------------------------------------------------")
		logging.info(str(datetime.now())+" Raspberry> Intento conectarme al ESP32")
		s.connect((serverMACAddress,port))
		while 1:
			data = s.recv(size)
			if data:
				strData = data.decode("utf-8")
				logging.info(str(datetime.now())+" Raspberry> Recibido: "+strData)
				lcd.lcd_display_strings(str(datetime.now()), strData)
				s.send("ACK\n".encode("utf-8"))
		s.close()
	except KeyboardInterrupt:
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion (CTRL-C)")
		lcd.lcd_display_strings(str(datetime.now()), "Servidor parado)")
		s.close()
		exit()
	except ConnectionResetError: 
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion")
	except ConnectionRefusedError:
		s.close()
		logging.info(str(datetime.now())+" Raspberry> Fallo")
		time.sleep(5)
 
	except:
		raise


