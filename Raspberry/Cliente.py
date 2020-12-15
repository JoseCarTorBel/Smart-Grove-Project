import socket
import subprocess
import logging
from datetime import datetime
import I2C_LCD_driver
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from GoogleDrive import GoogleDrive


# LCD lib
lcd=I2C_LCD_driver.lcd()


# GoogleDrive lib
goodr = GoogleDrive()

# Logging conf
logging.basicConfig( level=logging.DEBUG, filename='/home/pi/SmartGrove/Raspberry/Cliente.log')

# Bluetooth conf
serverMACAddress = 'F0:08:D1:C8:DB:FE'
port = 1
size=1024


class Trama:
	hora=""
	temperatura=-1
	humedad=-1
	def __init__(self,hor,tem,hum):
		self.hora=hor
		self.temperatura=tem
		self.humedad=hum
	def getTrama(self):
		return [self.hora,self.temperatura,self.humedad]




logging.info("=========================================================================")
while(1):
	recibido=[]
	tramas=0
	try:
		s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

		logging.info("----------------------------------------------------")
		lcd.lcd_display_strings(str(datetime.now()), "ESPERANDO AL CLIENTE")
		logging.info(str(datetime.now())+" Raspberry> Intento conectarme al ESP32")

		#s.connect((serverMACAddress,port))
		while 1:
			#data = s.recv(size)
			sleep(1)
			data="21#60"
			if data:
				strData = data.decode("UTF-8")
				if('#' in strData):
					recibido.append(Trama(str(datetime.now()),int(strData.split("#")[0]),int(strData.split("#")[1])))
					tramas+=1

					logging.info(str(datetime.now())+" Raspberry> Recibido: "+strData)
					lcd.lcd_display_strings(str(datetime.now()), str(strData))
					#s.send("ACK\n".encode("utf-8"))

					if(tramas%10==0):
						print(tramas)
						aux=10
						enviar=[]
						while(aux>=0):
							enviar.append(recibido[tramas-aux].getTrama())
							aux-=1
						print(enviar)
						#goodr.insertRows(enviar)
						

					
		s.close() #fin while

	except KeyboardInterrupt:
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion (CTRL-C)")
		lcd.lcd_display_strings(str(datetime.now()), "Cliente parado)")
		s.close()
		exit()
	except ConnectionResetError: 
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion")
		lcd.lcd_display_strings(str(datetime.now()), "Cierro conexion")
	except ConnectionRefusedError:
		s.close()
		logging.info(str(datetime.now())+" Raspberry> Fallo")
		lcd.lcd_display_strings(str(datetime.now()), "Fallo")
		time.sleep(5)
	except TimeoutError:
		s.close()
		logging.info(str(datetime.now())+" Raspberry> Fallo")
		lcd.lcd_display_strings(str(datetime.now()), "Fallo")
		time.sleep(5) 
	except:
		lcd.lcd_display_strings(str(datetime.now()), "ERROR-> LOG")
		raise


