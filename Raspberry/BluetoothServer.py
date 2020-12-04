import socket
import subprocess


def get_bt_mac():
        cmd = "hciconfig"
        device_id = "hci0" 
        status, output = subprocess.getstatusoutput(cmd)
        bt_mac = output.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
        print("Raspberry> Mac: " + bt_mac.lower())
        return bt_mac.lower()



status,output=subprocess.getstatusoutput("sudo sdptool add --channel=22 SP")
print(output)
hostMACAddress = get_bt_mac() 

port = 22
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)
except: 
    print("Closing socket")     
    client.close()
    s.close()

