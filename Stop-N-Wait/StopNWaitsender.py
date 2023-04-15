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
    global frame_to_send
    global seqNo
    global tkinter_status
    file = open("b.txt", "ab")
    file.seek(0)
    file.truncate(0)
    print(f'StopNWait Sender', end='', flush=True)
    no_of_frames = int(input('Enter No of frames to be sent : '))
    while no_of_frames > 0:
        canSend = False
        data = input('Enter Data to be trasffered to client : ')
        tkinter_status = []
        tkinter_status.extend([seqNo, data])
        while not canSend:
            packet_ack = packet_ack(data)
            rand_no = random.randint(1, 4)
            frame = Frame(packet_ack)
            from_physical_layer(packet_ack)
            to_network_layer(packet_ack)
            to_physical_layer(packet_ack)
            sock.sendto(pickle.dumps(packet_ack), ('localhost', 8025))
            send_timer.start()
            if rand_no == 1:
                ##Frame becomes corrupted
                print('Info : ', data)
                print('Seq NO : ', seqNo)
                print('Frame Lost')
                print('Resending the frame')
                tkinter_status.append('Frame Lost')
                send_timer.stop()
                print('------------------------------------------------------------------')
            elif rand_no == 2:
                print('Info : ', data)
                print('Seq NO : ', seqNo)
                print('TimeOut')
                print('Resending the Frame')
                tkinter_status.append('Timeout')
                send_timer.stop()
                print('------------------------------------------------------------------')
            elif rand_no == 3:
                print('Info : ', data)
                print('Seq NO : ', seqNo)
                acknowledgement, _ = sock.recvfrom(1024)
                acknowledgement = str(acknowledgement, 'utf-8')
                print(acknowledgement)
                send_timer.stop()
                tkinter_status.append('Acknowledgement Lost')
                print('------------------------------------------------------------------')
            elif rand_no == 4:
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
send()
sock.close()