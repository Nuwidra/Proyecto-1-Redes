import socket
import time
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


frame_to_send = 0
tkinter_status = []

def send(TIMEOUT_INTERVAL, SLEEP_INTERVAL, no_of_frames, data):
    global sock
    seqNo = 0
    send_timer = Timer(TIMEOUT_INTERVAL)
    file = open("b.txt", "ab")
    file.seek(0)
    file.truncate(0)
    print(f'Utopia Sender', end='', flush=True)
    while no_of_frames > 0:
        canSend = False
        tkinter_status = [seqNo, data]
        while not canSend:
            packet = Packet(data)
            frame = Frame(packet)
            from_network_layer(packet)
            sock.sendto(pickle.dumps(frame), RECEIVER_ADDR)
            canSend = True
            to_physical_layer(frame)
        pickle.dump(tkinter_status, file)
        no_of_frames -= 1
        seqNo += 1
    file.close()
    time.sleep(10)

## stop the sender
def stop():
    """
    stop the sender
    """
    print('Sender Stopped')
    # close the socket with error handling
    try:
        sock.close()
    except OSError:
        pass


