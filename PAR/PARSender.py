import socket
import pickle
import timer.timer
from events.events import *

RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)

def send_data():
    # get input from user
    num_frames = int(input("Enter the number of frames to send: "))
    data = input("Enter the data to send: ")

    from_network_layer(data)
    seq_no = 0
    for i in range(num_frames):
        # create packet with sequence number and data
        packet = [seq_no, data]
        to_physical_layer(packet)
        # send packet
        sock.sendto(pickle.dumps(packet), RECEIVER_ADDR)
        print(f"Sent packet with seqNo={seq_no}")
        # wait for ACK
        while True:
            from_physical_layer(packet)
            ack_packet, addr = sock.recvfrom(1024)
            ack = pickle.loads(ack_packet)
            ack_seq_no = ack[0]
            if ack_seq_no == seq_no:
                print(f"Received ACK with seqNo={ack_seq_no}")
                from_network_layer(packet)
                break
        # increment sequence number
        seq_no = (seq_no + 1) % 2

send_data()
sock.close()