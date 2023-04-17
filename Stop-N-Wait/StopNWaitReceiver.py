import pickle
import socket
from events.events import *
from frame.frame import Packet, Frame

RECEIVER_ADDR = ('localhost', 8025)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(RECEIVER_ADDR)

def receive():
    print(f'StopNWait Reciever', end='', flush=True)
    while True:
        packet_connect_address, addr = sock.recvfrom(1024)
        data_loads = pickle.loads(packet_connect_address)
        packet = Packet(data_loads)
        from_network_layer(packet)
        frame = Frame(packet)
        rand = packet.sequence_number
        to_physical_layer(frame)
        if rand == 4:
            print('Frame Received with seqNo: ', frame.sequence_number)
            packet_connect_address = (int(frame.sequence_number) + 1) % 2
            print('Acknowlegment ', packet_connect_address, ' sent')
            sock.sendto(bytes(str(packet_connect_address), 'utf-8'), ('localhost', 8000))
            print('------------------------------------------------------------------')
        elif rand == 3:
            print('Frame Received with seqNo: ', frame.sequence_number)
            packet_connect_address = 'Acknowledgement Lost'
            sock.sendto(bytes(str(packet_connect_address), 'utf-8'), ('localhost', 8000))
            print('------------------------------------------------------------------')
        elif rand == 1 or rand == 2:
            print('No Frame Received')
            print('------------------------------------------------------------------')
        else:
            break

# close the socket
def stop_receiver():
    sock.close()

