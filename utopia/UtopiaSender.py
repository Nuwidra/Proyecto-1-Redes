import socket
import time
import random
import pickle
from tkinter import *

from timer.timer import Timer

class Packet:
    def __init__(self, data):
        self.data = data

class Frame:
    def __init__(self, packet):
        self.type = 'frame'
        self.sequence_number = random.randint(0, 999)
        self.confirmation_number = packet.sequence_number
        self.data = packet.data


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)

TIMEOUT_INTERVAL = 0.5
SLEEP_INTERVAL = 0.05

send_timer = Timer(TIMEOUT_INTERVAL)

frame_to_send = 0
seqNo = 0
tkinter_status = []


def send():
    global sock
    global send_timer
    global frame_to_send
    global seqNo
    global tkinter_status
    f = open("b.txt", "ab")
    f.seek(0)
    f.truncate(0)

    print(f'\33]0;Utopia Sender\a', end='', flush=True)
    no_of_frames = int(input('Enter No of frames to be sent : '))

    while no_of_frames > 0:

        canSend = False
        data = input('Enter Data to be trasffered to client : ')
        tkinter_status = []
        tkinter_status.extend([seqNo, data])
        while not canSend:
            packet = []
            rand_no = random.randint(1, 4)

            packet.extend([seqNo, data, rand_no])
            sock.sendto(pickle.dumps(packet), ('localhost', 8025))
            canSend = True


        pickle.dump(tkinter_status, f)
        no_of_frames -= 1
        # sock.close()
    f.close()
    time.sleep(10)


send()
sock.close()

