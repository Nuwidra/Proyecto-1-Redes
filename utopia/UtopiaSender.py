import socket
import time
import pickle
from tkinter import *
from events.events import *
from frame.frame import Packet, Frame
from timer.timer import Timer
# from StopNWaitsender import send
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# receiver address and port number
RECEIVER_ADDR = ('localhost', 8026)
# create a UDP socket and bind it to the listening address
SENDER_ADDR = ('localhost', 8030)
# bind the socket to the listening address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to the listening address
sock.bind(SENDER_ADDR)

# send a packet to the socket
frame_to_send = 0
# loop indefinitely, receiving packets and sending acknowledgments
tkinter_status = []
# send a packet to the socket
def send(TIMEOUT_INTERVAL, SLEEP_INTERVAL, no_of_frames, data):
    # global variables
    global sock
    # create a new frame with a window size of 4
    seqNo = 0
    send_timer = Timer(TIMEOUT_INTERVAL)
    file = open("b.txt", "ab")
    file.seek(0)
    file.truncate(0)
    print(f'Utopia Sender', end='', flush=True)
    while no_of_frames > 0: # while there are frames to be sent
        canSend = False
        tkinter_status = [seqNo, data]
        while not canSend: # while the frame is not sent
            packet = Packet(data) # create packet
            frame = Frame(packet) # create frame
            from_network_layer(packet) # send packet to network layer
            sock.sendto(pickle.dumps(frame), RECEIVER_ADDR) # send frame to receiver
            canSend = True # frame is sent
            to_physical_layer(frame)
        pickle.dump(tkinter_status, file) # write the status to file
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


