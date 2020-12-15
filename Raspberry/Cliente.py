import socket
import subprocess
import logging
from datetime import datetime
import I2C_LCD_driver
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from GoogleDrive import GoogleDrive

lcd=I2C_LCD_driver.lcd()

goodr = GoogleDrive()

logging.basicConfig( level=logging.DEBUG, filename='/home/pi/SmartGrove/Raspberry/Cliente.log')

serverMACAddress = 'F0:08:D1:C8:DB:FE'



class Trama:
	hora=""
	temperatura=""
	humedad=""
	def __init__(self,hor,tem,hum):
		self.hora=hor
		self.temperatura=tem
		self.humedad=hum
	def getTrama(self):
		return [self.hora,self.temperatura,self.humedad]


port = 1
size=1024
logging.info("=========================================================================")
while(1):
	recibido=[]
	tramas=0
	try:
		s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
		logging.info("----------------------------------------------------")
		lcd.lcd_display_strings(str(datetime.now()), "ESPERANDO AL CLIENTE")
		logging.info(str(datetime.now())+" Raspberry> Intento conectarme al ESP32")
		s.connect((serverMACAddress,port))
		while 1:
			data = s.recv(size)
			if data:
				strData = data.decode("UTF-8")
				if('#' in strData):
					recibido.append(Trama(str(datetime.now()),strData.split("#")[0],strData.split("#")[1]))
					tramas+=1
					if(tramas%2==0):
						goodr.insertRow(recibido[tramas-1].getTrama())
						goodr.insertRow(recibido[tramas-2].getTrama())

					logging.info(str(datetime.now())+" Raspberry> Recibido: "+strData)
					lcd.lcd_display_strings(str(datetime.now()), str(strData))
					s.send("ACK\n".encode("utf-8"))
		s.close()
	except KeyboardInterrupt:
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion (CTRL-C)")
		lcd.lcd_display_strings(str(datetime.now()), "Cliente parado)")
		s.close()
		exit()
	except ConnectionResetError: 
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion")
	except ConnectionRefusedError:
		s.close()
		logging.info(str(datetime.now())+" Raspberry> Fallo")
		time.sleep(5)
	except TimeoutError:
		s.close()
		logging.info(str(datetime.now())+" Raspberry> Fallo")
		time.sleep(5) 
	except:
		raise


