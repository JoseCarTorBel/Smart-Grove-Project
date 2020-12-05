import socket
import subprocess
import logging
from datetime import datetime


def get_bt_mac():
        cmd = "hciconfig"
        device_id = "hci0" 
        status, output = subprocess.getstatusoutput(cmd)
        bt_mac = output.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
        #print("Raspberry> Mac: " + bt_mac.lower())
        logging.info(str(datetime.now())+" Raspberry> Mac: " + bt_mac.lower())
        return bt_mac.lower()




logging.basicConfig( level=logging.DEBUG, filename='/home/pi/Proyecto/Raspberry/Server.log')

status,output=subprocess.getstatusoutput("sudo sdptool add --channel=22 SP")

hostMACAddress = get_bt_mac() 

port = 22
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
while(1):
	try:
		#print("Raspberry> Espero conexion")
		logging.info(str(datetime.now())+" Raspberry> Espero conexion")
		client, address = s.accept()
		#print("Raspberry> Conexion aceptada")
		logging.info(str(datetime.now())+" Raspberry> Conexion aceptada")
		while 1:
			data = client.recv(size)
			if data:
				if(("killServer" in data.decode("utf-8"))):
					client.close()
					s.close()
					exit()
				logging.info(str(datetime.now())+" Raspberry> Recibido: "+data.decode("utf-8"))
				#print(data)
				client.send(data)
					
	except KeyboardInterrupt:
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
