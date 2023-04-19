import socket
import pickle
import random
from events.events import *

# define the sender and receiver IP addresses and port numbers
RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

# Receiver function is used to receive the frames from the sender.
def receiver() :
    print(f'GoBackN Receiver', end = '', flush = True)
    # This loop is used to receive the frames from the sender.
    while True :
        enable_network_layer() # enable the network layer
        packet_address,addr = sock.recvfrom(1024) # receive a packet from the sender
        packet_address = pickle.loads(packet_address) # deserialize the packet
        packet = [] # create a new packet
        m = int(packet_address[0]) # window size
        frame_send_at_instance = int(packet_address[1]) # number of frames sent at instance
        arr1 = packet_address[2] # array of frames sent at instance
        rw = int(packet_address[3]) # receive window
        f = int(packet_address[4]) # flag
        f1 = int(packet_address[5]) # flag
        if f != 5 : # if flag is not 5
            from_physical_layer(packet) # receive the packet from the physical layer
            for i in range(frame_send_at_instance) : # for each frame sent at instance
                if rw == int(arr1[i]) : # if receive window is equal to frame sent at instance
                    to_network_layer(packet) # send the packet to the network layer
                    print("Frame ",arr1[i]," is received correctly.")
                    print("--------------------------------------------------------------------------------")
                    rw = (rw+1)%m
                else : # if receive window is not equal to frame sent at instance
                    to_network_layer(packet) # send the packet to the network layer
                    print("Duplicate Frame ",arr1[i]," is discarded")
            a1 = random.randint(0,14) # generate a random number
            packet.extend([rw,a1]) # append the receive window and random number to the packet
            sock.sendto(pickle.dumps(packet),addr) # send the packet to the sender
        else :
            from_physical_layer(packet) # receive the packet from the physical layer
            for i in range(f1) :
                if rw == int(arr1[i]) : # if receive window is equal to frame sent at instance
                    to_network_layer(packet) # send the packet to the network layer
                    print("Frame ",arr1[i]," is received correctly.")
                    rw = (rw + 1)%m
                    print("--------------------------------------------------------------------------------")
                else :
                    to_network_layer(packet) # send the packet to the network layer
                    print("Duplicate Frame ",arr1[i]," is discarded.")
                    print("--------------------------------------------------------------------------------")
            packet.extend([rw,f1]) # append the receive window and random number to the packet
            sock.sendto(pickle.dumps(packet),addr)


# stop receiver
def stop_receiver() :
    disable_network_layer()
    sock.close()