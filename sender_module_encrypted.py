import socket
from time import sleep
import serial
from tcp_client_module import connection as enviar
from tcp_server_module import server as recibir
import configparser
import dhlib

config = configparser.ConfigParser()
config.read('config.ini')
COM = config['SERIAL']['COM']
PORT = config['SERIAL']['PORT']
ser = serial.Serial(PORT, COM, timeout=1)
sleep(2)

def main():

    interfaces = socket.getaddrinfo(
        host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]
    pub = 197
    priv = 199
    sleep(5)
    enviar("localhost",10001,int.to_bytes(pub, 1, "big"))
    pub2 = recibir("localhost",10002)
    own_partial = dhlib.dhPartialKey(pub,priv,pub2)
    enviar("localhost",10003,int.to_bytes(own_partial, 1, "big"))
    other_partial = recibir("localhost",10004)
    my_full = dhlib.dhFullKey(priv,pub2,other_partial)

    
   
    while True:
       
        line = ser.readline()
        if line:
            msg = b'sensor'
            payload = dhlib.dhEncrypt(line.decode()[0:-2],my_full)
            msg += payload.encode('utf-8')
        else:
            continue

        for ip in allips:
            print(f'sending on {ip}')
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(msg, ("255.255.255.255", 5005))
            sock.close()

        sleep(2)


try:
    main()
except KeyboardInterrupt:
    ser.close()
