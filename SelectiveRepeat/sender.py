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


def shipping_confirmation(size_buffer, lock, frames_without_confirmation, actual_ack_seq_num):
    socket_sender.bind(('', portA))
    while True:
        try:
            ack, _ = socket_sender.recvfrom(size_buffer)
            lock.acquire()
            ack_number = pickle.loads(ack)
            print("\nFrame Confirmed: ", ack_number)
            actual_ack_seq_num = ack_number
            frames_without_confirmation.remove(ack_number)
            lock.release()
        except Exception as e:
            print("Error: ", e)


def next_frame(frames_window, counter_window):
    next_frame_to_send = frames_window[counter_window]
    counter_window += 1
    return next_frame_to_send


def sender_window(packet, frame_type, frames_window, actual_seq_num):
    frame_to_send = Frame(random.choice(frame_type), actual_seq_num, -1, packet)
    frames_window.append(frame_to_send)
    actual_seq_num += 1


def sender(window_size, packet):
    counter_window = 0
    size_buffer = 1024
    frames_without_confirmation = []
    frames_window = []
    attempts = 0
    actual_seq_num = 0
    actual_ack_seq_num = -1
    lock = threading.Lock()
    network_layer_flag = True
    frame_type = [Packet.data,
                  Packet.CKSUM_ERR]

    attempts = (window_size + 1) / 2
    thread = threading.Thread(target=shipping_confirmation,
                              args=(size_buffer, lock, frames_without_confirmation, actual_ack_seq_num))
    thread.start()
    while True:
        if len(frames_window) < window_size and network_layer_flag:
            sender_window(packet, frame_type, frames_window, actual_seq_num)
        else:
            network_layer_flag = False
            time.sleep(1.5)
            lock.acquire()
            frame_to_send = next_frame(frames_window, counter_window)
            frames_without_confirmation.append(frame_to_send.sequenceNumber)
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
            if counter_window == window_size:
                frames_window.clear()
                counter_window = 0
                network_layer_flag = True


def retry_send(frameToSend, frames_without_confirmation, lock, frame_type, attempts):
    lock.acquire()
    if frameToSend.sequenceNumber not in frames_without_confirmation:
        lock.release()
        return
    frameToSend.packet = random.choice(frame_type)
    print("\nSending Again: ", frameToSend.sequenceNumber)
    serialized_frame = pickle.dumps(frameToSend)
    try:
        socket_sender.sendto(serialized_frame, (host, portB))
    except:
        print("The execution has ended")
        lock.release()
        return
    timer = threading.Timer(attempts, retry_send,
                            args=(frameToSend, frames_without_confirmation, lock, frame_type, attempts))
    timer.start()
    lock.release()

def stop_sender():
    socket_sender.close()

if __name__ == '__main__':
    data = "Hello World"
    sender(4, Packet.data)
