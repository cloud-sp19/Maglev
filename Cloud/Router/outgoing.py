import os
import random

from netfilterqueue import NetfilterQueue

from scapy.layers.dns import IP, UDP, TCP, conf

from scapy.all import send

sock = conf.L3socket()

def process_packet_netfilter(listener_packet):
    """
    Callback function for each packet received by netfilter
    """
    global sock

    packet = IP(listener_packet.get_payload())
    listener_packet.drop()

    if "IP" not in packet or packet[IP].dst == "127.0.0.1":
        return

    packet[IP].src = "10.1.0.1" # hide the endpoint IP

    # Force re-computation of the checksum since the header changed
    if "UDP" in packet:
        del packet[UDP].chksum
    if "TCP" in packet:
        del packet[TCP].chksum

    del packet[IP].chksum

    packet.show()

    sock.send(packet)


def run():
    os.system('iptables -t mangle -A POSTROUTING --protocol tcp --sport 54 -j NFQUEUE --queue-num 11')

    nfqueue = NetfilterQueue()
    nfqueue.bind(11, process_packet_netfilter)
    print("Outgoing NFQUEUE 11 is setup")

    try:
        nfqueue.run()
    except KeyboardInterrupt:
        os.system('iptables -t mangle -D POSTROUTING --protocol tcp --sport 54 -j NFQUEUE --queue-num 11')

if __name__ == '__main__':
    run()