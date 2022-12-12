import socket
from time import sleep
import serial
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
COM = config['SERIAL']['COM']
PORT = config['SERIAL']['PORT']
# print(COM)
ser = serial.Serial(PORT, COM, timeout=1)
sleep(2)


def main():

    interfaces = socket.getaddrinfo(
        host=socket.gethostname(), port=None, family=socket.AF_INET)
    allips = [ip[-1][0] for ip in interfaces]

    while True:
        line = ser.readline()
        if line:
            msg = b'sensor'
            msg += line
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
