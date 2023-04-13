import socket
import pickle
import random
from events.events import *
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

def receiver() :

    print(f'\33]0;GoBackN Receiver\a', end = '', flush = True)
    while True :
        enable_network_layer()
        pkt,addr = sock.recvfrom(1024)
        pkt = pickle.loads(pkt)
        packet = []
        m = int(pkt[0])
        frame_send_at_instance = int(pkt[1])
        arr1 = pkt[2]
        rw = int(pkt[3])
        f = int(pkt[4])
        f1 = int(pkt[5])

        if f != 5 :
            from_physical_layer(packet)
            for i in range(frame_send_at_instance) :
                if rw == int(arr1[i]) :
                    to_network_layer(packet)
                    print("--------------------------------------------------------------------------------")
                    print("Frame ",arr1[i]," is received correctly.")
                    rw = (rw+1)%m
                    print("--------------------------------------------------------------------------------")
                else :
                    to_network_layer(packet)
                    print("--------------------------------------------------------------------------------")
                    print("Duplicate Frame ",arr1[i]," is discarded")
                    print("--------------------------------------------------------------------------------")
                    
            a1 = random.randint(0,14)
            packet.extend([rw,a1])
            sock.sendto(pickle.dumps(packet),addr)

        else :
            from_physical_layer(packet)
            for i in range(f1) :
                if rw == int(arr1[i]) :
                    to_network_layer(packet)
                    print("--------------------------------------------------------------------------------")
                    print("Frame ",arr1[i]," is received correctly.")
                    rw = (rw + 1)%m
                    print("--------------------------------------------------------------------------------")

                else :
                    to_network_layer(packet)
                    print("--------------------------------------------------------------------------------")
                    print("Duplicate Frame ",arr1[i]," is discarded.")
                    print("--------------------------------------------------------------------------------")

            packet.extend([rw,f1])
            sock.sendto(pickle.dumps(packet),addr)


receiver()
sock.close()
