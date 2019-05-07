import os
import random

from netfilterqueue import NetfilterQueue

from scapy.layers.dns import IP, UDP, TCP, conf

from scapy.all import send

endpoints = [(65537, "10.3.2.1"), (65539, "10.3.2.2")] # endpoint array ip address and prime number

sock = conf.L3socket()

def del_checksum(packet):
    # Force re-computation of the checksum since the header changed
    if "UDP" in packet:
        del packet[UDP].chksum
    if "TCP" in packet:
        del packet[TCP].chksum

    del packet[IP].chksum

    return packet

def process_packet_netfilter(listener_packet):
    """
    Callback function for each packet received by netfilter
    """
    global endpoints
    global sock

    packet = IP(listener_packet.get_payload())
    listener_packet.drop()

    if "IP" not in packet or packet[IP].dst == "127.0.0.1" or "TCP" not in packet:
        return

    print("Incoming packet")
    packet[TCP].show()

    # Endpoint selection
    local_timestamp = None
    for option in packet[TCP].options:
        key, value = option

        if key == 'Timestamp':
            remote, local = value
            local_timestamp = local

    print("Local Timestamp: " + str(local_timestamp))

    if local_timestamp == 0 or local_timestamp == None: # for syn
        #print("Sending to all endpoints")
        # Send to one randomly
        randI = random.randint(0,1);

        # First Endpoint
        if randI == 0:
            packet[IP].dst = "10.3.2.1"
            packet = del_checksum(packet)
            sock.send(packet)  # Send packet to first endpoint
        else:
            # Second Endpoint
            packet[IP].dst = "10.3.2.2"  # Accepted packet will go to second point
            packet = del_checksum(packet)
            sock.send(packet) # Send packet to second endpoint
        return

    for endpoint in endpoints:
        prime, endpoint_ip = endpoint

        if (local_timestamp % prime) == 0: # for the rest of the packets in the flow
            print("Sending to endpoint " + endpoint_ip)
            packet[IP].dst = endpoint_ip

            packet = del_checksum(packet)

            sock.send(packet)


def run():
    os.system('iptables -t mangle -A PREROUTING --protocol tcp --dport 54 -j NFQUEUE --queue-num 10')

    nfqueue = NetfilterQueue()
    nfqueue.bind(10, process_packet_netfilter)
    print("NFQUEUE is setup")

    try:
        nfqueue.run()
    except KeyboardInterrupt:
        os.system('iptables -t mangle -D PREROUTING --protocol tcp --dport 54 -j NFQUEUE --queue-num 10')

if __name__ == '__main__':
    run()