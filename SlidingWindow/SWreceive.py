import socket
import pickle

from SlidingWindow.frame import Frame


def receive_packets(listen_ip, listen_port):
    # create a UDP socket and bind it to the listening address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))

    # create a new frame with a window size of 4
    frame = Frame(window_size=4)

    # loop indefinitely, receiving packets and sending acknowledgments
    while True:
        # receive a packet from the socket
        data, addr = sock.recvfrom(1024)
        packet = pickle.loads(data)
        # send an acknowledgment packet
        ack_packet = frame.receive_packet(packet)
        ack_data = pickle.dumps(ack_packet)
        sock.sendto(ack_data, addr)

    # close the socket
    sock.close()


# stop_sw_receiver
def stop_sw_receiver():
    global receiver
    receiver = False
