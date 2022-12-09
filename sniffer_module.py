import scapy.all as scapy
from scapy.layers.inet import UDP

def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=sniffed_packet)

def sniffed_packet(packet):
    if type(packet.payload.payload.payload) == scapy.packet.Raw:
        print(packet.payload.payload.payload)

def main():
    sniff("en0")

if __name__ == '__main__':
    main()