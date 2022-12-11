import scapy.all as scapy
import dhlib
from tcp_client_module import connection as enviar
from tcp_server_module import server as recibir


def sniff(interface):
    pub = 151
    priv = 157
    pub2 = recibir("localhost",10001)
    enviar("localhost",10002,int.to_bytes(pub, 1, "big"))
    own_partial = dhlib.dhPartialKey(pub2,priv,pub)
    other_partial = recibir("localhost",10003)
    enviar("localhost",10004,int.to_bytes(own_partial, 1, "big"))
    my_full = dhlib.dhFullKey(priv,pub,other_partial)
    mensaje = recibir("localhost",1005)
    print("mensaje: " + dhlib.dhDecrypt(str(mensaje),my_full))

    print("Sniffer:" + str(my_full))
    #scapy.sniff(iface=interface, store=False, prn=sniffed_packet)



#def sniffed_packet(packet):
    #if type(packet.payload.payload.payload) == scapy.packet.Raw:
    #    payload = bytes(packet.payload.payload.payload)
    #    if payload[0:6] == b'sensor':
    #        temp = float(payload[6:-2].decode())
    #        print(temp)


def main():
    sniff("en0")


if __name__ == '__main__':
    main()
