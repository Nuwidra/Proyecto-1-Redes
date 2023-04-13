import socket
import pickle
import timer.timer
from events.events import *
from frame.frame import Frame, Packet

RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)

def send_data():
    # get input from user
    num_frames = int(input("Enter the number of frames to send: "))
    data = input("Enter the data to send: ")

    # create initial packet with data
    packet = Packet(data)

    seq_no = 0
    for i in range(num_frames):
        # create frame with packet and sequence number
        frame = Frame(packet)
        frame.sequence_number = seq_no

        # send frame
        sock.sendto(pickle.dumps(frame), RECEIVER_ADDR)
        print(f"Sent frame with seqNo={seq_no}")

        # start timer for frame
        start_timer(frame.sequence_number)

        # wait for ACK
        while True:
            ack_packet, addr = sock.recvfrom(1024)
            ack = pickle.loads(ack_packet)
            if isinstance(ack, Frame) and ack.confirmation_number == seq_no:
                print(f"Received ACK with seqNo={ack.confirmation_number}")
                # stop timer for frame
                stop_timer(seq_no)
                break

        # increment sequence number
        seq_no = (seq_no + 1) % 2

        # update packet sequence number
        packet.sequence_number = seq_no

    # send empty frame to signal end of transmission
    end_frame = Frame(Packet(""))
    end_frame.sequence_number = seq_no
    sock.sendto(pickle.dumps(end_frame), RECEIVER_ADDR)

    sock.close()

send_data()
sock.close()