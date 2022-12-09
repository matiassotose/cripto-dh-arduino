import scapy.all as scapy


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet)


def sniffed_packet(packet):
    if type(packet.payload.payload.payload) == scapy.packet.Raw:
        payload = bytes(packet.payload.payload.payload)
        if payload[0:6] == b'sensor':
            temp = float(payload[6:-2].decode())
            print(temp)


def main():
    sniff("en0")


if __name__ == '__main__':
    main()
