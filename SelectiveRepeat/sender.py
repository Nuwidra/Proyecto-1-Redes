import time
from SelectiveRepeat.frame import Frame
from additional_resources import *
def next_frame():
    global counter_window
    next_frame_to_send = frames_window[counter_window]
    counter_window += 1
    return next_frame_to_send
def sender_window(packet):
    global actual_seq_num
    frame_to_send = Frame(random.choice(frame_type), actual_seq_num, -1, packet)
    frames_window.append(frame_to_send)
    actual_seq_num += 1
def sender(window_size=7):
    global network_layer_flag
    global actual_ack_seq_num
    global counter_window
    global attempts
    attempts = (window_size + 1) / 2
    thread = threading.Thread(target=shipping_confirmation, args=())
    thread.start()
    packet = str(input("Insert text:\n"))
    while True:
        if len(frames_window) < window_size and network_layer_flag:
            sender_window(packet)
        else:
            network_layer_flag = False
            time.sleep(1.5)
            lock.acquire()
            frame_to_send = next_frame()
            frames_without_confirmation.append(frame_to_send.sequenceNumber)
            serializedFrame = pickle.dumps(frame_to_send)
            print("\nSending: ", frame_to_send.sequenceNumber)
            print("+++++++++++++++++")
            try:
                socket_sender.sendto(serializedFrame, (host, portB))
            except:
                print("The execution has ended")
                return
            timer = threading.Timer(attempts, retry_send, args=(frame_to_send,))
            timer.start()
            lock.release()
            if counter_window == window_size:
                frames_window.clear()
                counter_window = 0
                network_layer_flag = True
def retry_send(frameToSend):
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
    timer = threading.Timer(attempts, retry_send, args=(frameToSend,))
    timer.start()
    lock.release()
sender()