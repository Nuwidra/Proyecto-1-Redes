import pickle
import sys
import socket
import random
import time
from events.events import *
from frame.frame import Packet, Frame

RECEIVER_ADDR = ('localhost', 8025)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

def receive():
    print(f'\33]0;StopNWait Reciever\a', end='', flush=True)

    while True:
        pkt, addr = sock.recvfrom(1024)
        a_data = pickle.loads(pkt)
        packet = Packet(a_data)
        from_network_layer(packet)
        frame = Frame(packet)
        rand = packet.sequence_number
        to_physical_layer(frame)
        if rand == 4:
            print('Frame Received with seqNo: ', frame.sequence_number)
            pkt = (int(frame.sequence_number) + 1) % 2
            print('Acknowlegment ', pkt, ' sent')
            sock.sendto(bytes(str(pkt), 'utf-8'), ('localhost', 8000))
            print('------------------------------------------------------------------')
            # break

        elif rand == 3:
            print('Frame Received with seqNo: ', frame.sequence_number)
            pkt = 'Acknowledgement Lost'
            sock.sendto(bytes(str(pkt), 'utf-8'), ('localhost', 8000))
            print('------------------------------------------------------------------')

        elif rand == 1 or rand == 2:
            print('No Frame Received')
            print('------------------------------------------------------------------')

        else:
            break
    # sock.close()
    # time.sleep(10)

receive()
sock.close()