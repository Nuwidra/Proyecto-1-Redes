import pickle
import socket
from SelectiveRepeat.frame import Frame, Packet

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
portA = 8004
portB = 8006
receiver_socket.bind(('', portB))

def receiver(window_size=7):
    total_size = 8192
    frame_size = 0
    frame_list = []
    expected_seq_num = 0
    frame_size = (window_size + 1) / 2
    while True:
        try:
            frame_was_obtained, _ = receiver_socket.recvfrom(total_size)
            frame_was_obtained = pickle.loads(frame_was_obtained)
            sequence_number = frame_was_obtained.sequenceNumber
            print("\nProcesando: ", sequence_number)
            if expected_seq_num == sequence_number and not frame_was_obtained.packet == Packet.CKSUM_ERR:
                print("Info: ", frame_was_obtained.packetInfo)
                receiver_socket.sendto(pickle.dumps(sequence_number), (host, portA))
                expected_seq_num += 1
                if len(frame_list) > 0:
                    print("Frames en el Buffer: ", [item.sequenceNumber for item in frame_list])
                    expected_seq_num += len(frame_list)
                    frame_list.clear()
                    print("Frame expected: ", expected_seq_num)
                else:
                    print("No frame here")
            elif sequence_number >= expected_seq_num - frame_size / 2 and sequence_number <= expected_seq_num + frame_size / 2 and len(
                    frame_list) < frame_size:
                if not frame_was_obtained.packet == Packet.CKSUM_ERR:
                    print("Info: ", frame_was_obtained.packetInfo)


                    frame_list.append(frame_was_obtained)
                    print("Frame esperado: ", expected_seq_num)
                    receiver_socket.sendto(pickle.dumps(sequence_number), (host, portA))
        except Exception as e:
            print("FATAL ERROR WITH THE FRAME")

def stop_receiver():
    receiver_socket.close()

if __name__ == '__main__':
    receiver()