import os

from netfilterqueue import NetfilterQueue

from scapy.layers.dns import IP

from scapy.all import send

def build_response_packet(listener_packet):
    listener_packet[IP].dst = "10.1.0.2"


def process_packet_netfilter(listener_packet):
    """
    Callback function for each packet received by netfilter
    """

    packet = IP(listener_packet.get_payload())
    listener_packet.drop()

    response_packet = build_response_packet(packet)
    send(response_packet, verbose=0)


def run():
    os.system('iptables -t mangle -A PREROUTING -j NFQUEUE --queue-num 10')

    nfqueue = NetfilterQueue()
    nfqueue.bind(10, process_packet_netfilter)
    print("NFQUEUE is setup")


if __name__ == '__main__':
    run()