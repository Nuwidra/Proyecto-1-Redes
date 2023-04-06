import socket
import time
import random
import pickle
from tkinter import *

from timer import Timer

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

def send() :

    global sock
    global send_timer
    global frame_to_send
    global seqNo
    global tkinter_status
    f = open("b.txt","ab")
    f.seek(0)
    f.truncate(0)
    
    print(f'\33]0;StopNWait Sender\a', end = '', flush = True)
    no_of_frames = int(input('Enter No of frames to be sent : '))

    while no_of_frames > 0 :
    
        canSend = False
        data = input('Enter Data to be trasffered to client : ')
        tkinter_status = []    
        tkinter_status.extend([seqNo,data])
        while not canSend:
            packet = []
            rand_no = random.randint(1,4)
                
            packet.extend([seqNo,data,rand_no])
            sock.sendto(pickle.dumps(packet),('localhost',8025))
            send_timer.start()

            ## Frame sent..ACK received
            ack,_ = sock.recvfrom(1024)
            ack = str(ack,'utf-8')
            print('Info : ',data)
            print('Seq NO : ',seqNo)
            print('Acknowledgement No : ',ack,' received')
            send_timer.stop()
            canSend = True
            seqNo = (seqNo + 1) % 2
            tkinter_status.append('Acknowledgement Received')
            print('------------------------------------------------------------------')

    
        pickle.dump(tkinter_status,f)
        no_of_frames -= 1
        #sock.close()
    f.close()
    time.sleep(10)

    
send()
sock.close()

