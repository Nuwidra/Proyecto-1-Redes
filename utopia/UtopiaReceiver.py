import pickle
import socket
from events.events import *
from frame.frame import Packet, Frame
RECEIVER_ADDR = ('localhost', 8026)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

def receive():
    """
    reciver function to receive the data from sender
    """
    print(f'Utopia Reciever', end='', flush=True)
    while True: # wait for frame from sender
        wait_for_event('frame_arrival') # wait for frame from sender
        pkt, addr = sock.recvfrom(1024) # receive frame from sender
        DATA = pickle.loads(pkt) # deserialize frame
        packet = Packet(DATA.data) # create packet
        frame = Frame(packet) # create frame
        from_physical_layer(frame) # send frame to network layer
        to_network_layer(packet) # send packet to transport layer
        print('Frame Received with seqNo: ', frame.sequence_number)
        print('Content : ', frame.data)
        print('------------------------------------------------------------------')

## stop the receiver
def stop():
    """
    stop the reciever
    """
    print('Receiver Stopped')
    # close the socket with error handling
    try:
        sock.close()
    except OSError:
        pass






