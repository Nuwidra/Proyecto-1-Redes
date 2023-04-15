from pprint import pprint
import threading, pickle, socket, time, random
from src import *

#Main function, it manages all functions to establish the selective repetitive protocol
def senderSelectiveRepetitive(windowSize=7):
    global NETWORK_LAYER_READY
    global CURRENT_ACK_SEQUENCE_NUMBER
    global WINDOW_COUNTER
    global RETRY_TIMER
    
    RETRY_TIMER = (windowSize + 1) / 2
    thread = threading.Thread(target=confirmedSent, args=())
    thread.start()
    packet = str(input("Ingrese mensaje: "))
    while True:
        if len(WINDOW_FRAMES) < windowSize and NETWORK_LAYER_READY:
            setWindowSender(packet)
        else: 
            NETWORK_LAYER_READY = False
            time.sleep(1.5)
            
            LOCK.acquire()
            
            frameToSend = nextFrame()
            FRAMES_WITHOUT_CONFIRMATION.append(frameToSend.sequenceNumber)
            serializedFrame = pickle.dumps(frameToSend)
            
            print("____________________________")
            print("\nSending: ", frameToSend.sequenceNumber, "\nType: ", frameToSend.kind)
            
            try:
                senderSocket.sendto(serializedFrame, (host, portB))
            except:
                print("The execution has ended")
                return
            
            timer = threading.Timer(RETRY_TIMER, retry_send, args=(frameToSend,))
            timer.start()
            
            LOCK.release()
            
            if WINDOW_COUNTER == windowSize:
                WINDOW_FRAMES.clear()
                WINDOW_COUNTER = 0
                NETWORK_LAYER_READY = True

senderSelectiveRepetitive()