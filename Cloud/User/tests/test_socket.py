from scapy.layers.dns import IP, TCP

from scapy.all import send, sr1

import random

import socket

import time

import threading

def experiment(flow_no, flow_index):
    for k in range(0, 10):  # sample points
        time1 = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

        sock.connect(("10.1.0.1", 54))

        sock.send(b'hello')

        sock.close()
        elapsedTime = time.time() - time1
        print(str(flow_no) + ":" + str(flow_index) + ":" + str(k) + ":" + str(elapsedTime))

def run():


    # Number of flows to test
    for i in range(0, 100):

        threads = []

        # Create the threads, where each has i flows simultaneous
        for j in range (0, i):
            threads.append(threading.Thread(target=experiment, args=(i,j,)))


        # start the threads
        for j in range(0, i):
            threads[j].start()

        # wait until they all finish
        for j in range(0, i):
            threads[j].join()



if __name__ == '__main__':
    run()