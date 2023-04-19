import pickle
import socket
from events.events import *
from frame.frame import Packet, Frame
# receiver address and port number
RECEIVER_ADDR = ('localhost', 8025)
# create a UDP socket and bind it to the listening address
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to the listening address
sock.bind(RECEIVER_ADDR)
# receive a packet from the socket
def receive():
    print(f'StopNWait Reciever', end='', flush=True)
    # loop indefinitely, receiving packets and sending acknowledgments
    while True: # loop indefinitely, receiving packets and sending acknowledgments
        # packet_connect_address = (int(frame.sequence_number) + 1) % 2
        packet_connect_address, addr = sock.recvfrom(1024)
        # data_loads for packet and frame
        data_loads = pickle.loads(packet_connect_address)
        # packet is created
        packet = Packet(data_loads)
        # packet is sent to network layer
        from_network_layer(packet)
        # frame is created
        frame = Frame(packet)
        # frame is sent to physical layer
        rand = packet.sequence_number
        # to_physical_layer(frame) is sent to physical layer
        to_physical_layer(frame)
        # if frame is in order, then
        if rand == 4: # if frame is in order, then
            print('Frame Received with seqNo: ', frame.sequence_number)
            packet_connect_address = (int(frame.sequence_number) + 1) % 2
            print('Acknowlegment ', packet_connect_address, ' sent')
            sock.sendto(bytes(str(packet_connect_address), 'utf-8'), ('localhost', 8000))
            print('------------------------------------------------------------------')
        elif rand == 3: # if frame is out of order, then
            print('Frame Received with seqNo: ', frame.sequence_number)
            packet_connect_address = 'Acknowledgement Lost'
            sock.sendto(bytes(str(packet_connect_address), 'utf-8'), ('localhost', 8000))
            print('------------------------------------------------------------------')
        elif rand == 1 or rand == 2: # if frame is out of order, then
            print('No Frame Received')
            print('------------------------------------------------------------------')
        else:
            break

# close the socket
def stop_receiver():
    sock.close()

