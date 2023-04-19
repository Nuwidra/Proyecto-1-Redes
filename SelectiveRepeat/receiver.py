import pickle
import socket
from SelectiveRepeat.frame import Frame, Packet
# receiver_socket is used to create a socket.
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# host is used to get the host name.
host = socket.gethostname()
# portA is used to bind the socket to the sender.
portA = 8004
# portB is used to bind the socket to the receiver.
portB = 8006
# bind the socket to the receiver.
receiver_socket.bind(('', portB))
# receiver function is used to receive the frames from the sender.
def receiver(window_size=7):
    # total_size is used to get the total size of the frame.
    total_size = 8192
    # expected_seq_num is used to get the expected sequence number.
    frame_size = 0
    # frame_list is used to store the frames.
    frame_list = []
    # This loop is used to receive the frames from the sender.
    expected_seq_num = 0
    # frame_size is used to get the frame size.
    frame_size = (window_size + 1) / 2
    # This loop is used to receive the frames from the sender.
    while True:
        try: # try to receive frame
            # frame was obtained is used to get the frame from the sender.
            frame_was_obtained, _ = receiver_socket.recvfrom(total_size)
            # frame was obtained is used to deserialize the frame.
            frame_was_obtained = pickle.loads(frame_was_obtained)
            # sequence_number is used to get the sequence number of the frame.
            sequence_number = frame_was_obtained.sequenceNumber
            # confirmation_number is used to get the confirmation number of the frame.
            print("\nProcesando: ", sequence_number)
            # if frame is in order, then send ack and process frame
            if expected_seq_num == sequence_number and not frame_was_obtained.packet == Packet.CKSUM_ERR: # if frame is in order, then
                print("Info: ", frame_was_obtained.packetInfo)
                # send ack to sender for frame
                receiver_socket.sendto(pickle.dumps(sequence_number), (host, portA))
                # increment expected sequence number
                expected_seq_num += 1
                # frame list is cleared
                if len(frame_list) > 0: # if there are frames in the buffer, then
                    print("Frames en el Buffer: ", [item.sequenceNumber for item in frame_list])
                    # expected_seq_num is incremented
                    expected_seq_num += len(frame_list)
                    # frame list is cleared
                    frame_list.clear()
                    print("Frame expected: ", expected_seq_num)
                else: # if there are no frames in the buffer, then
                    print("No frame here")
            # sequence number is in the buffer and frame is not corrupted then process frame
            elif sequence_number >= expected_seq_num - frame_size / 2 and sequence_number <= expected_seq_num + frame_size / 2 and len(
                    frame_list) < frame_size: # if frame is in the buffer, then
                # if frame is not corrupted, then process frame
                if not frame_was_obtained.packet == Packet.CKSUM_ERR: # if frame is not corrupted, then
                    print("Info: ", frame_was_obtained.packetInfo)
                    # send ack to sender for frame
                    frame_list.append(frame_was_obtained)
                    print("Frame esperado: ", expected_seq_num)
                    receiver_socket.sendto(pickle.dumps(sequence_number), (host, portA))
        except Exception as e: # if frame is corrupted, then
            print("FATAL ERROR WITH THE FRAME")
# stop receiver function is used to stop the receiver.
def stop_receiver():
    receiver_socket.close()
# main function is used to run the receiver.
if __name__ == '__main__':
    receiver()