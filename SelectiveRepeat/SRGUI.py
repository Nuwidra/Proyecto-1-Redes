from tkinter import *
from threading import Thread
from SelectiveRepeat.sender import sender, stop_sender
from SelectiveRepeat.receiver import receiver, stop_receiver

# create a window
window = Tk()

# set the title
window.title("Selective Repeat Protocol")

# set the size
window.geometry('400x300')

# create labels
window_size_label = Label(window, text="Window Size:")
window_size_label.grid(column=0, row=0)

packet_label = Label(window, text="Packet:")
packet_label.grid(column=0, row=1)

# create entry fields
window_size_entry = Entry(window)
window_size_entry.grid(column=1, row=0)

packet_entry = Entry(window)
packet_entry.grid(column=1, row=1)

# create button to send data
def send_data():
    sender_thread = Thread(target=sender, args=(int(window_size_entry.get()), packet_entry.get()))
    sender_thread.start()

send_button = Button(window, text="Send", command=send_data)
send_button.grid(column=1, row=2)

# create button to receive data
def receive_data():
    receiver_thread = Thread(target=receiver)
    receiver_thread.start()

receive_button = Button(window, text="Receive", command=receive_data)
receive_button.grid(column=1, row=3)

# create button to stop sender and receiver
def stop_data():
    stop_sender()
    stop_receiver()

stop_button = Button(window, text="Stop", command=stop_data)
stop_button.grid(column=1, row=4)

# run the window
window.mainloop()