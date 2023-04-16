# import the necessary classes and functions
import socket
import pickle


# define the sender and receiver IP addresses and port numbers
from SlidingWindow.SWsend import send_packets
from SlidingWindow.SWreceive import receive_packets
from SlidingWindow.frame import Packet

sender_ip = '127.0.0.1'
sender_port = 5000
receiver_ip = '127.0.0.1'
receiver_port = 6000

# create a list of Packet objects to send
packets = [
    Packet(seq_num=0, data=b'Hello'),
    Packet(seq_num=1, data=b'World'),
    Packet(seq_num=2, data=b'How'),
    Packet(seq_num=3, data=b'Are'),
    Packet(seq_num=4, data=b'You'),
    Packet(seq_num=5, data=b'Today')
]

# start the receiver in a separate thread
import threading
receiver_thread = threading.Thread(target=receive_packets, args=(receiver_ip, receiver_port))
receiver_thread.start()

# wait a bit for the receiver to start up
import time
time.sleep(1)

# send the packets from the sender
send_packets(packets, receiver_ip, receiver_port)

# wait for the receiver to finish processing the packets
receiver_thread.join()