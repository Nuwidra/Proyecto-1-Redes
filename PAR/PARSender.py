import socket
import pickle
from events.events import *
from frame.frame import Frame, Packet
RECEIVER_ADDR = ('localhost',8009)
SENDER_ADDR = ('localhost', 8001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)


def send_data(num_frames,data):
    packet = Packet(data) # create packet
    seq_no = 0 # initialize sequence number
    for i in range(num_frames):
        frame = Frame(packet) # create frame
        frame.sequence_number = seq_no # set sequence number
        sock.sendto(pickle.dumps(frame), RECEIVER_ADDR) # send frame to receiver
        print(f"Sent frame with seqNo={seq_no}")
        start_timer(frame.sequence_number)
        # wait for ACK
        while True:
            ack_packet, addr = sock.recvfrom(1025) # receive ACK from receiver
            ack = pickle.loads(ack_packet) # deserialize ACK
            if isinstance(ack, Frame) and ack.confirmation_number == seq_no: # if ACK is in order, then
                print(f"Received ACK with seqNo={ack.confirmation_number}")
                stop_timer(seq_no)
                break
        seq_no = (seq_no + 1) % 2 # increment sequence number
        packet.sequence_number = seq_no # set sequence number of packet
    end_frame = Frame(Packet("")) # create end frame
    end_frame.sequence_number = seq_no # set sequence number
    sock.sendto(pickle.dumps(end_frame), RECEIVER_ADDR) # send end frame to receiver

def stop_sender():
    sock.close()