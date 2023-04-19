import socket
import pickle
from events.events import *
from frame.frame import Frame, Packet
RECEIVER_ADDR = ('localhost', 8009)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)
# receiver function is used to receive the frames from the sender.
def receive_data():
    print("Receiver started")
    expected_seq_no = 0
    # This loop is used to receive the frames from the sender.
    while True:
        # frame_packet is used to receive the frame from the sender.
        frame_packet, addr = sock.recvfrom(1024) # receive frame from sender
        frame = pickle.loads(frame_packet) # deserialize frame
        # frame is an ack
        if frame.data == "": # if frame is an ack, then
            break
        # frame sequence number is equal to expected sequence number
        if frame.sequence_number == expected_seq_no: # if frame is in order, then
            from_physical_layer(frame.data)
            print(f"Received: {frame.data}")
            ack = Frame(Packet(""))
            ack.type = "ack"
            ack.sequence_number = expected_seq_no
            ack.confirmation_number = expected_seq_no
            sock.sendto(pickle.dumps(ack), ('localhost', 8001))
            expected_seq_no = (expected_seq_no + 1) % 2
        # frame sequence number is not equal to expected sequence number
        else: # if frame is out of order, then
            print(f"Discarding out-of-order frame with seqNo: {frame.sequence_number}")
# stop receiver function is used to stop the receiver.
def stop_receiver():
    sock.close()



