import socket
import random
import pickle
import time
from events.events import *
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)
tkinter_status = []

tot_frames = 16
window_size = 3
total_number_of_frames = pow(2, window_size)
frame_number = 0
frame_send_at_instance = total_number_of_frames // 2
send_window = 0
receive_window = 0
array_to_store_the_frames_to_be_sent = []
array_to_store = []
size_of_the_array = 0
for i in range(tot_frames) :
    array_to_store.append(frame_number)
    frame_number = (frame_number + 1) % total_number_of_frames


def sender() :
    global total_number_of_frames
    global send_window,size_of_the_array
    global receive_window
    global frame_send_at_instance
    global array_to_store,total_frames
    global array_to_store_the_frames_to_be_sent
    file = open("l.txt","ab")
    file.seek(0)
    file.truncate(0)
    enable_network_layer()
    ch = 'y'
    print(f'GoBackN Sender', end = '', flush = True)
    while ch == 'y' and size_of_the_array < tot_frames :
        tkinter_status = []
        array_to_store_the_frames_to_be_sent = []
        packet = []
        j = 0
        to_physical_layer(packet)
        if tot_frames - size_of_the_array < 4 :
            from_network_layer(packet)
            frame_send_at_instance = tot_frames - size_of_the_array
        for i in range(send_window, (send_window + frame_send_at_instance)):
            to_network_layer(packet)
            array_to_store_the_frames_to_be_sent.append(array_to_store[i])
            j += 1
            tkinter_status.append(array_to_store[i])
        for i in range(j) :
            from_network_layer(packet)
            print("Frame  ", array_to_store_the_frames_to_be_sent[i], " is sent")
        print("--------------------------------------------------------------------------------")
        random_initial = random.randint(0,9)
        random_frame_instance = random.randint(0,frame_send_at_instance-1)
        packet.extend([total_number_of_frames, frame_send_at_instance, array_to_store_the_frames_to_be_sent, receive_window, random_initial, random_frame_instance])
        sock.sendto(pickle.dumps(packet),('localhost',8025))
        if random_initial != 5 :
            from_network_layer(packet)
            from_physical_layer(packet)
            ack,_ = sock.recvfrom(1024)
            ack = pickle.loads(ack)
            receive_window = int(ack[0])
            a1 = int(ack[1])
            if a1 >= 0 and a1 <= 3 :
                for k in range(len(array_to_store)) :
                    if array_to_store_the_frames_to_be_sent[k] != array_to_store_the_frames_to_be_sent[a1] :
                        print("Acknowledgement of Frame", array_to_store_the_frames_to_be_sent[k], " is recieved")
                        print("--------------------------------------------------------------------------------")
                    else :
                        break
                print("Acknowledgement of Frame ", array_to_store_the_frames_to_be_sent[a1], " is lost")
                print("--------------------------------------------------------------------------------")
                tkinter_status.append(["Acknowledgement Lost", array_to_store_the_frames_to_be_sent[a1]])
                temp = (send_window + frame_send_at_instance) % total_number_of_frames
                comp = 0
                if (temp == 0) :
                    comp = 7
                if int(array_to_store_the_frames_to_be_sent[a1]) == comp or int(array_to_store_the_frames_to_be_sent[a1]) == temp-1:
                    send_window = (send_window + 3) % total_number_of_frames
                    size_of_the_array += 3
                else :
                    send_window = (send_window + frame_send_at_instance) % total_number_of_frames
                    size_of_the_array += 4
            else :
                to_network_layer(packet)
                send_window = (send_window + frame_send_at_instance) % total_number_of_frames
                print("All Four Frames are Acknowledged")
                print("--------------------------------------------------------------------------------")
                size_of_the_array += 4
                tkinter_status.append(["Acknowledgement Received","All"])
        else :
            to_network_layer(packet)
            ack,_ = sock.recvfrom(1024)
            ack = pickle.loads(ack)
            receive_window = int(ack[0])
            random_frame_instance = int(ack[1])
            ld = random.randint(0,1)
            if ld == 0 :
                print("Frame ", array_to_store_the_frames_to_be_sent[random_frame_instance], " is damaged.")
                tkinter_status.append(["Frame Damaged", array_to_store_the_frames_to_be_sent[random_frame_instance]])
                print("--------------------------------------------------------------------------------")
            else :
                print("Frame ", array_to_store_the_frames_to_be_sent[random_frame_instance], " is lost")
                tkinter_status.append(["Frame Lost", array_to_store_the_frames_to_be_sent[random_frame_instance]])
                print("--------------------------------------------------------------------------------")
            for i in range(random_frame_instance+1,frame_send_at_instance) :
                print("Frame ", array_to_store_the_frames_to_be_sent[i], " is discarded")
            print("-------------TIMEOUT-------------")
            tkinter_status.append(["Timeout","All"])
            send_window = array_to_store_the_frames_to_be_sent[random_frame_instance]
        pickle.dump(tkinter_status,file)
        ch = input('Send Again(y/n) : ')
        if ch != 'y':
            enable_network_layer()
            break
    disable_network_layer();
    file.close()
    time.sleep(2)
sender()
sock.close()
