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
    print(f'\33]0;Utopia Reciever\a', end='', flush=True)

    while True:
        wait_for_event('frame_arrival')


        pkt, addr = sock.recvfrom(1024)
        a_data = pickle.loads(pkt)
        packet = Packet(a_data.data)
        frame = Frame(packet)
        from_physical_layer(frame)
        to_network_layer(packet)

        print('Frame Received with seqNo: ', frame.sequence_number)
        print('Content : ', frame.data)
        print('------------------------------------------------------------------')
        # break

    # sock.close()
    # time.sleep(10)


receive()
sock.close()