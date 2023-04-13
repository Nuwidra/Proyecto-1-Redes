import socket
import pickle
from events.events import *

RECEIVER_ADDR = ('localhost', 8025)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

expected_seq_no = 0

while True:
    pkt, addr = sock.recvfrom(1024)
    packet = pickle.loads(pkt)
    seq_no = packet[0]
    data = packet[1]

    if seq_no == expected_seq_no:
        from_physical_layer(packet)
        # received expected packet
        print(f"Received: {data}")
        # send ACK
        ack_packet = [expected_seq_no]
        sock.sendto(pickle.dumps(ack_packet), ('localhost', 8000))
        # increment expected sequence number
        expected_seq_no = (expected_seq_no + 1) % 2
        to_physical_layer(packet)
    else:
        # received out-of-order packet, discard and wait for retransmission
        print(f"Discarding out-of-order packet with seq_no: {seq_no}")

sock.close()