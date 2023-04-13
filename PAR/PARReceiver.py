import socket
import pickle
from events.events import *
from frame.frame import Frame, Packet

RECEIVER_ADDR = ('localhost', 8025)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

expected_seq_no = 0

while True:
    # receive frame over socket and unpickle it
    frame_packet, addr = sock.recvfrom(1024)
    frame = pickle.loads(frame_packet)

    # check if it's the end of the transmission
    if frame.data == "":
        break

    # check if the sequence number matches the expected value
    if frame.sequence_number == expected_seq_no:
        # send packet to the network layer
        from_physical_layer(frame.data)
        print(f"Received: {frame.data}")
        # send ACK
        ack = Frame(Packet(""))
        ack.type = "ack"
        ack.sequence_number = expected_seq_no
        ack.confirmation_number = expected_seq_no
        sock.sendto(pickle.dumps(ack), ('localhost', 8000))
        # increment expected sequence number
        expected_seq_no = (expected_seq_no + 1) % 2
    else:
        # received out-of-order frame, discard and wait for retransmission
        print(f"Discarding out-of-order frame with seqNo: {frame.sequence_number}")

sock.close()