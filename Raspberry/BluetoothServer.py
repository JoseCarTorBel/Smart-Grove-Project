import socket
import subprocess
import logging
from datetime import datetime
import I2C_LCD_driver
from time import *


def get_bt_mac():
        cmd = "hciconfig"
        device_id = "hci0"
        status, output = subprocess.getstatusoutput(cmd)
        bt_mac = output.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
        logging.info(str(datetime.now())+" Raspberry> Mac: " + bt_mac.lower())
        lcd.lcd_display_string(bt_mac.lower(), 1)
        return bt_mac.lower()


def emparejar(dirMac):
	pass


lcd=I2C_LCD_driver.lcd()
logging.basicConfig( level=logging.DEBUG, filename='/home/pi/SmartGrove/Raspberry/Server.log')

status,output=subprocess.getstatusoutput("sudo sdptool add --channel=22 SP")

hostMACAddress = get_bt_mac() 

port = 22
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
logging.info("=========================================================================")
while(1):
	try:
		logging.info("----------------------------------------------------")
		logging.info(str(datetime.now())+" Raspberry> Espero conexion")
		lcd.lcd_display_string(str(datetime.now()), 1)
		lcd.lcd_display_string("Espero conexion", 2)
		client, address = s.accept()
		logging.info(str(datetime.now())+" Raspberry> Conexion aceptada de la direccion: "+str(address[0]))
		lcd.lcd_display_string(str(datetime.now()), 1)
		lcd.lcd_display_string("Conexion aceptada", 2)
		client.send("Para parar conexion usa el comando: killServer\n".encode("UTF-8"))
		while 1:
			data = client.recv(size)
			if data:
				strData = data.decode("utf-8")
				logging.info(str(datetime.now())+" Raspberry> Recibido: "+strData)
				lcd.lcd_display_string(str(datetime.now()), 1)
				lcd.lcd_display_string(strData, 2)
				if("MAC=" in strData):
					emparejar(strData.split("=")[1])
				if(("killServer" in strData)):
					client.send("PARANDO SERVIDOR".encode("utf-8"))
					logging.info(str(datetime.now())+" Raspberry> Cierro conexion (killServer)")
					lcd.lcd_display_string("Servidor parado", 1)
					client.close()
					s.close()
					exit()
				client.send("ACK\n".encode("utf-8"))
					
	except KeyboardInterrupt:
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion (CTRL-C)")
		lcd.lcd_display_string(str(datetime.now()), 1)
		lcd.lcd_display_string("Servidor parado", 2)
		client.close()
		s.close()
		exit()
	except ConnectionResetError: 
		#print("Raspberry> Cierro conexion")
		logging.info(str(datetime.now())+" Raspberry> Cierro conexion")
		client.close()
		#s.close()
	except:
		raise
