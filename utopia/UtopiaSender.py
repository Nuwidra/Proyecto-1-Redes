import socket
import time
import random
import pickle
from tkinter import *

from events.events import *
from frame.frame import Packet, Frame
from timer.timer import Timer

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)

TIMEOUT_INTERVAL = float(input('Ingrese la probabildad de TIMEOUT_INTERVAL: ')) # 0.5
SLEEP_INTERVAL = float(input('Ingrese la probabildad de SLEEP_INTERVAL: ')) # 0.05

send_timer = Timer(TIMEOUT_INTERVAL)

frame_to_send = 0
seqNo = 0
tkinter_status = []


def send():
    global sock
    global send_timer
    global seqNo
    f = open("b.txt", "ab")
    f.seek(0)
    f.truncate(0)

    print(f'\33]0;Utopia Sender\a', end='', flush=True)
    no_of_frames = int(input('Enter No of frames to be sent : '))

    while no_of_frames > 0:
        canSend = False
        data = input('Enter Data to be transferred to client : ')
        tkinter_status = [seqNo, data]

        while not canSend:
            packet = Packet(data)
            frame = Frame(packet)
            from_network_layer(packet)
            sock.sendto(pickle.dumps(frame), RECEIVER_ADDR)
            canSend = True
            to_physical_layer(frame)

        pickle.dump(tkinter_status, f)
        no_of_frames -= 1
        seqNo += 1

    f.close()
    time.sleep(10)


send()
sock.close()