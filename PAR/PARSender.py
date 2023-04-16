import socket
import pickle
from events.events import *
from frame.frame import Frame, Packet
RECEIVER_ADDR = ('localhost',8009)
SENDER_ADDR = ('localhost', 8001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)


def send_data(num_frames,data):
    packet = Packet(data)
    seq_no = 0
    for i in range(num_frames):
        frame = Frame(packet)
        frame.sequence_number = seq_no
        sock.sendto(pickle.dumps(frame), RECEIVER_ADDR)
        print(f"Sent frame with seqNo={seq_no}")
        start_timer(frame.sequence_number)
        # wait for ACK
        while True:
            ack_packet, addr = sock.recvfrom(1025)
            ack = pickle.loads(ack_packet)
            if isinstance(ack, Frame) and ack.confirmation_number == seq_no:
                print(f"Received ACK with seqNo={ack.confirmation_number}")
                stop_timer(seq_no)
                break
        seq_no = (seq_no + 1) % 2
        packet.sequence_number = seq_no
    end_frame = Frame(Packet(""))
    end_frame.sequence_number = seq_no
    sock.sendto(pickle.dumps(end_frame), RECEIVER_ADDR)

def stop_sender():
    sock.close()