import pickle
import time
import threading, socket, random

from SelectiveRepeat.frame import Frame
from SelectiveRepeat.frame import Packet

# Socket for the sender to send the frames
socket_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()

# Ports for the sender and receiver
portA = 8004
portB = 8006

# Bind the socket to the receiver
def shipping_confirmation(size_buffer, lock, frames_without_confirmation, actual_ack_seq_num):
    socket_sender.bind(('', portA))
    # This loop is used to receive the frames from the sender.
    while True:
        try:
            # ack is used to get the ack from the receiver.
            ack, _ = socket_sender.recvfrom(size_buffer)
            # ack is used to deserialize the ack.
            lock.acquire()
            # ack_number is used to get the ack number.
            ack_number = pickle.loads(ack)
            # print the ack number.
            print("\nFrame Confirmed: ", ack_number)
            # actual_ack_seq_num is used to get the actual ack sequence number.
            actual_ack_seq_num = ack_number
            # remove the frame from the frames without confirmation.
            frames_without_confirmation.remove(ack_number)
            # print the frames without confirmation.
            lock.release()
        # except the exception.
        except Exception as e:
            print("Error: ", e)

# This function is used to send the frames to the receiver.
def next_frame(frames_window, counter_window):
    next_frame_to_send = frames_window[counter_window]
    counter_window += 1
    return next_frame_to_send

# This function is used to send the frames to the receiver.
def sender_window(packet, frame_type, frames_window, actual_seq_num):
    frame_to_send = Frame(random.choice(frame_type), actual_seq_num, -1, packet)
    frames_window.append(frame_to_send)
    actual_seq_num += 1

# This function is used to send the frames to the receiver.
def sender(window_size, packet):
    # counter_window is used to get the counter window.
    counter_window = 0
    # size_buffer is used to get the size buffer.
    size_buffer = 1024
    # frames_without_confirmation is used to get the frames without confirmation.
    frames_without_confirmation = []
    # frames_window is used to get the frames window.
    frames_window = []
    # attempts is used to get the attempts.
    attempts = 0
    # actual_seq_num is used to get the actual sequence number.
    actual_seq_num = 0
    # actual_ack_seq_num is used to get the actual ack sequence number.
    actual_ack_seq_num = -1
    # lock is used to get the lock.
    lock = threading.Lock()
    # network_layer_flag is used to get the network layer flag.
    network_layer_flag = True
    # frame_type is used to get the frame type.
    frame_type = [Packet.data,
                  Packet.CKSUM_ERR]
    # attempts is used to get the attempts.
    attempts = (window_size + 1) / 2
    # thread is used to get the thread.
    thread = threading.Thread(target=shipping_confirmation,
                              args=(size_buffer, lock, frames_without_confirmation, actual_ack_seq_num))
    thread.start()
    # This loop is used to send the frames to the receiver.
    while True:
        # This if is used to send the frames to the receiver.
        if len(frames_window) < window_size and network_layer_flag:
            sender_window(packet, frame_type, frames_window, actual_seq_num)
        # This else is used to send the frames to the receiver.
        else:
            # network_layer_flag is used to get the network layer flag.
            network_layer_flag = False
            # This if is used to send the frames to the receiver.
            time.sleep(1.5)
            # This if is used to send the frames to the receiver.
            lock.acquire()
            # frame_to_send is used to get the frame to send.
            frame_to_send = next_frame(frames_window, counter_window)
            # counter_window is used to get the counter window.
            frames_without_confirmation.append(frame_to_send.sequenceNumber)
            # counter_window is used to get the counter window.
            serializedFrame = pickle.dumps(frame_to_send)
            print("\nSending: ", frame_to_send.sequenceNumber)
            print("+++++++++++++++++")
            try:
                socket_sender.sendto(serializedFrame, (host, portB))
            except:
                print("The execution has ended")
                return
            timer = threading.Timer(attempts, retry_send,
                                    args=(frame_to_send, frames_without_confirmation, lock, frame_type, attempts))
            timer.start()
            lock.release()
            # This counter window is used to get the counter window.
            if counter_window == window_size:
                frames_window.clear()
                counter_window = 0
                network_layer_flag = True

# retry_send is used to retry the send.
def retry_send(frameToSend, frames_without_confirmation, lock, frame_type, attempts):
    lock.acquire()
    # This if is used to retry the send.
    if frameToSend.sequenceNumber not in frames_without_confirmation:
        lock.release()
        return
    # This else is used to retry the send.
    frameToSend.packet = random.choice(frame_type)
    print("\nSending Again: ", frameToSend.sequenceNumber)
    # serialized_frame is used to get the serialized frame.
    serialized_frame = pickle.dumps(frameToSend)
    # This try is used to retry the send.
    try:
        socket_sender.sendto(serialized_frame, (host, portB))
    # except the exception.
    except:
        print("The execution has ended")
        lock.release()
        return
    timer = threading.Timer(attempts, retry_send,
                            args=(frameToSend, frames_without_confirmation, lock, frame_type, attempts))
    timer.start()
    lock.release()
# stop_sender is used to stop the sender.
def stop_sender():
    socket_sender.close()
# This is the main function.
if __name__ == '__main__':
    data = "Hello World"
    sender(4, Packet.data)
