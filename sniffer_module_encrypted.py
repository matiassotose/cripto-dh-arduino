import scapy.all as scapy
import auxilary_modules.dhlib as dhlib
from tcp.tcp_client_module import connection as enviar
from tcp.tcp_server_module import server as recibir
import tempfile
from auxilary_modules.upload_aws_module import upload

pub = 151
priv = 157
pub2 = recibir("localhost", 10001)
enviar("localhost", 10002, int.to_bytes(pub, 1, "big"))
own_partial = dhlib.dhPartialKey(pub2, priv, pub)
other_partial = recibir("localhost", 10003)
enviar("localhost", 10004, int.to_bytes(own_partial, 1, "big"))
my_full = dhlib.dhFullKey(priv, pub, other_partial)

temp_array = []


def sniff(interface):
    print("Sniffer:" + str(my_full))
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet, stop_filter=stop_sniffing)


def sniffed_packet(packet):
    if type(packet.payload.payload.payload) == scapy.packet.Raw:
        payload = bytes(packet.payload.payload.payload)
        if payload[0:6] == b'sensor':
            msg = dhlib.dhDecrypt(payload[6:].decode(), my_full)
            print(msg)
            temp_array.append(msg)

def stop_sniffing(p):
    if len(temp_array) >19:
        temp_file = tempfile.NamedTemporaryFile()
        for value in temp_array:
            temp_file.write(bytes(value,'utf8')+b'\n')
        temp_file.seek(0)
        upload(temp_file.name)
        temp_file.close()
        return True
    else:
        return False


def main():
    sniff("en0")


if __name__ == '__main__':
    main()
