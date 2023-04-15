import pickle
import socket
from events.events import *
from frame.frame import Packet, Frame
RECEIVER_ADDR = ('localhost', 8025)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)
def receive():
    print(f'Utopia Reciever', end='', flush=True)
    while True:
        wait_for_event('frame_arrival')
        pkt, addr = sock.recvfrom(1024)
        DATA = pickle.loads(pkt)
        packet = Packet(DATA.data)
        frame = Frame(packet)
        from_physical_layer(frame)
        to_network_layer(packet)
        print('Frame Received with seqNo: ', frame.sequence_number)
        print('Content : ', frame.data)
        print('------------------------------------------------------------------')
receive()
sock.close()