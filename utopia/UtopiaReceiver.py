import pickle
import sys
import socket
import random
import time

RECEIVER_ADDR = ('localhost', 8025)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)


def receive():
    print(f'\33]0;Utopia Reciever\a', end='', flush=True)

    while True:
        pkt, addr = sock.recvfrom(1024)
        a_data = pickle.loads(pkt)
        seq_no = a_data[0]

        print('Frame Received with seqNo: ', seq_no)
        print('Content : ', a_data[1])
        print('------------------------------------------------------------------')
        # break

    # sock.close()
    # time.sleep(10)


receive()
sock.close()