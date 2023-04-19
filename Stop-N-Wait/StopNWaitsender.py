import socket
import time
import random
import pickle
from tkinter import *
from events.events import *
from frame.frame import Packet, Frame
from timer.timer import Timer
# sock in sender
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# receiver address and port number
RECEIVER_ADDR = ('localhost', 8025)
# create a UDP socket and bind it to the listening address
SENDER_ADDR = ('localhost', 8000)
# bind the socket to the listening address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to the listening address
sock.bind(SENDER_ADDR)
# send a packet to the socket
def send(TIMEOUT_INTERVAL, SLEEP_INTERVAL, no_of_frames, data):
    global sock
    # create a new frame with a window size of 4
    send_timer = Timer(TIMEOUT_INTERVAL)
    frame_to_send = 0
    # loop indefinitely, receiving packets and sending acknowledgments
    seqNo = 0
    # file open in append mode
    file = open("b.txt", "ab")
    file.seek(0)
    file.truncate(0)
    print(f'StopNWait Sender', end='', flush=True)
    while no_of_frames > 0: # while there are frames to be sent
        canSend = False
        tkinter_status = []
        # if frame is in order, then
        tkinter_status.extend([seqNo, data])
        while not canSend: # while the frame is not sent
            packet_ack = Packet(data)
            # packet_ack is sent to network layer
            rand_no = random.randint(1, 4)
            frame = Frame(packet_ack)
            # frame is sent to physical layer
            from_physical_layer(packet_ack)
            # frame is sent to physical layer
            to_network_layer(packet_ack)
            # frame is sent to physical layer
            to_physical_layer(packet_ack)
            # frame is sent to physical layer
            sock.sendto(pickle.dumps(packet_ack), ('localhost', 8025))
            send_timer.start()
            # if frame is in order, then
            if rand_no == 1: # if the frame is not corrupted
                ##Frame becomes corrupted
                print('Info : ', data)
                print('Seq NO : ', seqNo)
                print('Frame Lost')
                print('Resending the frame')
                tkinter_status.append('Frame Lost')
                send_timer.stop()
                print('------------------------------------------------------------------')
            elif rand_no == 2: # if the frame is not corrupted
                print('Info : ', data)
                print('Seq NO : ', seqNo)
                print('TimeOut')
                print('Resending the Frame')
                tkinter_status.append('Timeout')
                send_timer.stop()
                print('------------------------------------------------------------------')
            elif rand_no == 3: # if the frame is not corrupted
                print('Info : ', data)
                print('Seq NO : ', seqNo)
                acknowledgement, _ = sock.recvfrom(1024)
                acknowledgement = str(acknowledgement, 'utf-8')
                print(acknowledgement)
                send_timer.stop()
                tkinter_status.append('Acknowledgement Lost')
                print('------------------------------------------------------------------')
            elif rand_no == 4: # if the frame is not corrupted
                acknowledgement, _ = sock.recvfrom(1024)
                acknowledgement = str(acknowledgement, 'utf-8')
                print('Info : ', data)
                print('Seq NO : ', seqNo)
                print('Acknowledgement No : ', acknowledgement, ' received')
                send_timer.stop()
                canSend = True
                seqNo = (seqNo + 1) % 2
                tkinter_status.append('Acknowledgement Received')
                print('------------------------------------------------------------------')
        pickle.dump(tkinter_status, file)
        no_of_frames -= 1
    file.close()
    time.sleep(10)

# close the socket
def stop_sender():
    sock.close()