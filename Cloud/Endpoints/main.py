import os
import random
import sys

from netfilterqueue import NetfilterQueue

from scapy.layers.dns import IP, UDP, TCP, raw, conf

from scapy.layers.inet import IPOption_Security

from scapy.all import send

prime_number = int(sys.argv[1])

sock = conf.L3socket()

def process_packet_netfilter(listener_packet):
    """
    Callback function for each packet received by netfilter
    """

    global prime_number

    packet = IP(listener_packet.get_payload())
    listener_packet.drop()

    if "IP" not in packet or packet[IP].dst == "127.0.0.1":
        return

    # IP options - failure
    #packet[IP].options = IPOption_Security(security=0x0001)

    #del packet[IP].ihl
    #del packet[IP].len

    # TCP options - success

    new_options = []
    for option in packet[TCP].options:
        key, value = option

        if key == 'Timestamp':
            local, remote = value
            print("Previous Local Timestamp:" + str(local))

            while True: # OS: monotonically increases it (lets increase it to a multiple of our prime num
                if (local % prime_number) == 0:
                    break
                local += 1

            print("New Local Timestamp:" + str(local))

            new_options.append(('Timestamp', (local, remote)))
        else:
            new_options.append(option)

    packet[TCP].options = new_options

    # Force re-computation of the checksum since the header changed
    if "UDP" in packet:
        del packet[UDP].chksum
    if "TCP" in packet:
        del packet[TCP].chksum

    del packet[IP].chksum

    packet = IP(raw(packet))
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