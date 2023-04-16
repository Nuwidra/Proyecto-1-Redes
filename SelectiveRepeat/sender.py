import pickle, socket, time, random
from SelectiveRepeat.frame import Kind, Frame
from variables_sender import *
def nextFrame():
    global counter_window
    nextFrameToSend = frames_window[counter_window]
    counter_window += 1
    return nextFrameToSend
def confirmedSent():
    global actual_ack_seq_num
    socket_sender.bind(('', portA))
    while True:
        try:
            ack, _ = socket_sender.recvfrom(size_buffer)
            lock.acquire()
            ackNum = pickle.loads(ack)
            print("\nFrame Confirmed: ", ackNum)
            actual_ack_seq_num = ackNum
            frames_without_confirmation.remove(ackNum)
            lock.release()
        except Exception as e:
            print("Error: ", e)
def setWindowSender(packet):
    global actual_seq_num
    frameToSend = Frame(random.choice(frame_type), actual_seq_num, -1, packet)
    frames_window.append(frameToSend)
    actual_seq_num += 1
def retry_send(frameToSend):
    lock.acquire()
    if frameToSend.sequenceNumber not in frames_without_confirmation:
        lock.release()
        return
    frameToSend.kind = random.choice(frame_type)
    print("____________________________")
    print("\nSending Again: ", frameToSend.sequenceNumber, "\nType: ", frameToSend.kind)
    serializedFrame = pickle.dumps(frameToSend)
    try:
        socket_sender.sendto(serializedFrame, (host, portB))
    except:
        print("The execution has ended")
        lock.release()
        return
    timer = threading.Timer(attempts, retry_send, args=(frameToSend,))
    timer.start()
    lock.release()
def sender(windowSize=7):
    global network_layer_flag
    global actual_ack_seq_num
    global counter_window
    global attempts
    attempts = (windowSize + 1) / 2
    thread = threading.Thread(target=confirmedSent, args=())
    thread.start()
    packet = str(input("Insert text:\n"))
    while True:
        if len(frames_window) < windowSize and network_layer_flag:
            setWindowSender(packet)
        else:
            network_layer_flag = False
            time.sleep(1.5)
            lock.acquire()
            frameToSend = nextFrame()
            frames_without_confirmation.append(frameToSend.sequenceNumber)
            serializedFrame = pickle.dumps(frameToSend)
            print("____________________________")
            print("\nSending: ", frameToSend.sequenceNumber, "\nType: ", frameToSend.kind)
            try:
                socket_sender.sendto(serializedFrame, (host, portB))
            except:
                print("The execution has ended")
                return
            timer = threading.Timer(attempts, retry_send, args=(frameToSend,))
            timer.start()
            lock.release()
            if counter_window == windowSize:
                frames_window.clear()
                counter_window = 0
                network_layer_flag = True
sender()