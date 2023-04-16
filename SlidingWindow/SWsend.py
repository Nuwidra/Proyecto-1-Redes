import socket
import pickle

def send_packets(packets, dest_ip, dest_port):
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # set the socket timeout to 1 second
    sock.settimeout(1.0)

    # send each packet to the destination
    for packet in packets:
        # serialize the packet using pickle
        serialized_packet = pickle.dumps(packet)
        # send the packet to the destination
        sock.sendto(serialized_packet, (dest_ip, dest_port))
        # wait for an acknowledgment packet
        while True:
            try:
                ack_data, _ = sock.recvfrom(1024)
                ack_packet = pickle.loads(ack_data)
                if ack_packet.seq_num == packet.seq_num + 1:
                    # received correct acknowledgment packet
                    break
            except socket.timeout:
                # timed out waiting for acknowledgment packet
                pass

    # close the socket
    sock.close()

# stop_sw_sender
def stop_sw_sender():
    global sender
    sender = False

