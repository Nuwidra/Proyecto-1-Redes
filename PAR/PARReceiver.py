import socket
import pickle
from events.events import *
from frame.frame import Frame, Packet
RECEIVER_ADDR = ('localhost', 8009)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

def receive_data():
    print("Receiver started")
    expected_seq_no = 0
    while True:
        frame_packet, addr = sock.recvfrom(1024)
        frame = pickle.loads(frame_packet)
        if frame.data == "":
            break
        if frame.sequence_number == expected_seq_no:
            from_physical_layer(frame.data)
            print(f"Received: {frame.data}")
            ack = Frame(Packet(""))
            ack.type = "ack"
            ack.sequence_number = expected_seq_no
            ack.confirmation_number = expected_seq_no
            sock.sendto(pickle.dumps(ack), ('localhost', 8001))
            expected_seq_no = (expected_seq_no + 1) % 2
        else:
            print(f"Discarding out-of-order frame with seqNo: {frame.sequence_number}")

def stop_receiver():
    sock.close()



