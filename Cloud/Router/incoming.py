import os
import random

from netfilterqueue import NetfilterQueue

from scapy.layers.dns import IP, UDP, TCP, conf

from scapy.layers.inet import IPOption_Security

from scapy.all import send

sock = conf.L3socket()

def process_packet_netfilter(listener_packet):
    """
    Callback function for each packet received by netfilter
    """
    global sock

    packet = IP(listener_packet.get_payload())
    listener_packet.drop() # drop the packet, send the modified packet instead later on

    if "IP" not in packet or packet[IP].dst == "127.0.0.1" or packet[TCP].flags == "R":
        return

    randomNumber = random.randint(1, 2) # Either 1 or 2, kinda replicating ECMP, send to both with equal probability
    print("Random Number:" + str(randomNumber))
    if randomNumber == 1:
        packet[IP].dst = "10.2.1.1" # Load Balancer 1
    elif randomNumber == 2:
        packet[IP].dst = "10.2.1.2" # Load Balancer 2

    # Force re-computation of the checksum since the header changed
    if "UDP" in packet:
        del packet[UDP].chksum
    if "TCP" in packet:
        del packet[TCP].chksum

    del packet[IP].chksum

    packet.show()

    sock.send(packet) # send the packet

def run():
    # put the packets on queue 10 as long as they match the requirements
    os.system('iptables -t mangle -A PREROUTING --protocol tcp --dport 54 -j NFQUEUE --queue-num 10')

    nfqueue = NetfilterQueue()
    # packets on the queue 10 should be processed with that function
    nfqueue.bind(10, process_packet_netfilter) # process: change the destination to one of the LBs
    print("NFQUEUE is setup")

    try:
        nfqueue.run() # process the packets, continue the pipeline
    except KeyboardInterrupt:
        os.system('iptables -t mangle -D PREROUTING --protocol tcp --dport 54 -j NFQUEUE --queue-num 10')


if __name__ == '__main__':
    run()