import socket
import random
import pickle
import time
from events.events import *
# Receiver address and sender address
RECEIVER_ADDR = ('localhost', 8025)
SENDER_ADDR = ('localhost', 8000)
# Socket creation for receiver
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SENDER_ADDR)
# sender function is used to send the frames to the receiver.
def sender():
    # Variables declaration and initialization
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
    # This loop is used to send the frames to the receiver.
    for i in range(tot_frames):
        # If the size of the array is equal to the number of frames sent at instance
        array_to_store.append(frame_number)
        frame_number = (frame_number + 1) % total_number_of_frames
    # Open the file to store the frames sent at instance
    file = open("l.txt","ab")
    file.seek(0)
    file.truncate(0)
    enable_network_layer()
    ch = 'y'
    print(f'GoBackN Sender', end = '', flush = True)
    # senderLoop() is a function that is called to send the frames to the receiver.
    senderLoop(array_to_store, ch, file, frame_send_at_instance, receive_window, send_window, size_of_the_array,
               tot_frames, total_number_of_frames)
    # disable_network_layer() is a function that is called to disable the network layer.
    disable_network_layer();
    file.close()
    time.sleep(2)

# This function is used to send the frames to the receiver in loop.
def senderLoop(array_to_store, ch, file, frame_send_at_instance, receive_window, send_window, size_of_the_array,
               tot_frames, total_number_of_frames):
    # This while loop is used to send the frames to the receiver with size of the array.
    while ch == 'y' and size_of_the_array < tot_frames:
        array_to_store_the_frames_to_be_sent = []
        packet = []
        j = 0
        to_physical_layer(packet) # to_physical_layer() is a function that is called to send the frame to the physical layer
        # This if condition is used to check if the number of frames to be sent is less than 4.
        if tot_frames - size_of_the_array < 4: # if the number of frames to be sent is less than 4, then send all the frames
            from_network_layer(packet)
            frame_send_at_instance = tot_frames - size_of_the_array
        # This for loop is used to send the frames to the receiver.
        for i in range(send_window, (send_window + frame_send_at_instance)):
            to_network_layer(packet)
            array_to_store_the_frames_to_be_sent.append(array_to_store[i])
            j += 1
        # This for loop is used to send the frames to the receiver.
        for i in range(j):
            from_network_layer(packet)
            print("Frame  ", array_to_store_the_frames_to_be_sent[i], " is sent")
        print("--------------------------------------------------------------------------------")
        # random_initial is used to generate the random number.
        random_initial = random.randint(0, 9)
        # random_frame_instance is used to generate the random number.
        random_frame_instance = random.randint(0, frame_send_at_instance - 1)
        packet.extend(
            [total_number_of_frames, frame_send_at_instance, array_to_store_the_frames_to_be_sent, receive_window,
             random_initial, random_frame_instance])
        sock.sendto(pickle.dumps(packet), ('localhost', 8025))
        # This if condition is used to check if the random number is not 5.
        if random_initial != 5: # if the random number is not 5, then the acknowledgement is lost
            from_network_layer(packet)
            from_physical_layer(packet)
            # ack is used to store the acknowledgement ack is a list.
            ack, _ = sock.recvfrom(1024)
            ack = pickle.loads(ack)
            receive_window = int(ack[0])
            a1 = int(ack[1])
            # This if condition is used to check if the acknowledgement is not lost.
            if a1 >= 0 and a1 <= 3: # if the acknowledgement is not lost, then the acknowledgement is recieved
                # This for loop is used to print the acknowledgement.
                for k in range(len(array_to_store)):
                    # This if condition is used to check if the acknowledgement is not lost.
                    if array_to_store_the_frames_to_be_sent[k] != array_to_store_the_frames_to_be_sent[a1]:
                        print("Acknowledgement of Frame", array_to_store_the_frames_to_be_sent[k], " is recieved")
                        print("--------------------------------------------------------------------------------")
                    else:
                        break
                print("Acknowledgement of Frame ", array_to_store_the_frames_to_be_sent[a1], " is lost")
                print("--------------------------------------------------------------------------------")
                temp = (send_window + frame_send_at_instance) % total_number_of_frames
                comp = 0
                # This if condition is used to check if the frame is the last frame.
                if (temp == 0): # if the frame is the last frame, then the next frame to be sent is 0
                    comp = 7
                # This if condition is used to check if the acknowledgement is not lost.
                if int(array_to_store_the_frames_to_be_sent[a1]) == comp or int(
                        array_to_store_the_frames_to_be_sent[a1]) == temp - 1: # if the frame is the last frame, then the next frame to be sent is 0
                    send_window = (send_window + 3) % total_number_of_frames
                    size_of_the_array += 3
                # This if condition is used to check if the acknowledgement is not lost.
                else: # if the frame is not the last frame, then the next frame to be sent is the next frame
                    send_window = (send_window + frame_send_at_instance) % total_number_of_frames
                    size_of_the_array += 4
            # This else condition is used to check if the acknowledgement is lost.
            else: # if the acknowledgement is lost, then the acknowledgement is not recieved
                to_network_layer(packet)
                send_window = (send_window + frame_send_at_instance) % total_number_of_frames
                print("All Four Frames are Acknowledged")
                print("--------------------------------------------------------------------------------")
                size_of_the_array += 4
        # This else condition is used to check if the random number is 5.
        else: # if the random number is 5, then the acknowledgement is damaged
            to_network_layer(packet)
            ack, _ = sock.recvfrom(1024)
            ack = pickle.loads(ack)
            receive_window = int(ack[0])
            random_frame_instance = int(ack[1])
            ld = random.randint(0, 1)
            # id == 0 is used to check if the random number is 0.
            if ld == 0: # if the random number is 0, then the acknowledgement is damaged
                print("Frame ", array_to_store_the_frames_to_be_sent[random_frame_instance], " is damaged.")
                print("--------------------------------------------------------------------------------")
            # id == 1 is used to check if the random number is 1.
            else: # if the random number is 1, then the acknowledgement is lost
                print("Frame ", array_to_store_the_frames_to_be_sent[random_frame_instance], " is lost")
                print("--------------------------------------------------------------------------------")
            # This for loop is used to print the discarded frames.
            for i in range(random_frame_instance + 1, frame_send_at_instance):
                print("Frame ", array_to_store_the_frames_to_be_sent[i], " is discarded")
            print("-------------TIMEOUT-------------")
            send_window = array_to_store_the_frames_to_be_sent[random_frame_instance]
        # pickle is used to dump the packet.
        pickle.dump(packet, file)
        ch = input('Send Again(y/n) : ')
        # ch != 'y' is used to check if the user does not want to send more frames.
        if ch != 'y': # if the user does not want to send more frames, then the sender is disabled
            enable_network_layer()
            break


#stop sender and close socket
def disable_network_layer():
    print("Sender is disabled")
    sock.close()


