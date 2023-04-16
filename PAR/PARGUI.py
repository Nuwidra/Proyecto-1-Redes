from tkinter import *
import threading
from PAR.PARSender import send_data, stop_sender
from PAR.PARReceiver import receive_data, stop_receiver

# create a window
window = Tk()

# set the title
window.title("PAR Protocol")

# set the size
window.geometry('400x300')

# create labels
no_frames_label = Label(window, text="No of frames to be sent:")
no_frames_label.grid(column=0, row=0)

data_label = Label(window, text="Data to be transferred:")
data_label.grid(column=0, row=1)

# create entry fields
no_frames_entry = Entry(window)
no_frames_entry.grid(column=1, row=0)

data_entry = Entry(window)
data_entry.grid(column=1, row=1)

# create button to send data
send_button = Button(window, text="Send", command=lambda: send_data(
    int(no_frames_entry.get()),
    data_entry.get()
))
send_button.grid(column=1, row=2)

# create button to receive data
def receive_wrapper():
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

receive_button = Button(window, text="Receive", command=receive_wrapper)
receive_button.grid(column=1, row=3)

# create button to stop sender and receiver
stop_button = Button(window, text="Stop", command=lambda: [stop_sender(), stop_receiver()])
stop_button.grid(column=1, row=4)



# run the window
window.mainloop()