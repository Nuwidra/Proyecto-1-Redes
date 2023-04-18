from tkinter import *
import threading
from SlidingWindow.SWsend import send_packets, stop_sw_sender
from SlidingWindow.SWreceive import receive_packets
from SlidingWindow.frame import Packet

# create a window
window = Tk()

# set the title
window.title("Sliding Window Protocol")

# set the size
window.geometry('400x300')


no_packets_label = Label(window, text="No of packets to be sent:")
no_packets_label.grid(column=0, row=2)

packet_data_label = Label(window, text="Packet Data:")
packet_data_label.grid(column=0, row=3)

# create entry fields
no_packets_entry = Entry(window)
no_packets_entry.grid(column=1, row=2)

packet_data_entry = Entry(window)
packet_data_entry.grid(column=1, row=3)

# create function to run send in a separate thread
def send_thread():
    packets = []
    sender_ip = '127.0.0.1'
    sender_port = 5000
    receiver_ip = '127.0.0.1'
    receiver_port = 6000
    for i in range(int(no_packets_entry.get())):
        packets.append(Packet(seq_num=i, data=packet_data_entry.get().encode()))
    send_packets(packets, receiver_ip, receiver_port)

# create button to send data
send_button = Button(window, text="Send", command=lambda: threading.Thread(target=send_thread).start())
send_button.grid(column=1, row=4)

# create function to run receive in a separate thread
def receive_thread():
    receiver_ip = '127.0.0.1'
    receiver_port = 6000
    receive_packets(receiver_ip, receiver_port)

# create button to receive data
receive_button = Button(window, text="Receive", command=lambda: threading.Thread(target=receive_thread).start())
receive_button.grid(column=1, row=5)

# create button to stop sender
stop_button = Button(window, text="Stop", command=stop_sw_sender)
stop_button.grid(column=1, row=6)

# run the window
window.mainloop()