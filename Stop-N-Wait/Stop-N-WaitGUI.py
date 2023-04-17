from tkinter import *
import threading
from StopNWaitReceiver import receive, stop_receiver
from StopNWaitsender import send, stop_sender

# create a window
window = Tk()

# set the title
window.title("Stop N Wait Protocol")

# set the size
window.geometry('400x300')

# create labels
timeout_label = Label(window, text="TIMEOUT_INTERVAL:")
timeout_label.grid(column=0, row=0)

sleep_label = Label(window, text="SLEEP_INTERVAL:")
sleep_label.grid(column=0, row=1)

no_frames_label = Label(window, text="No of frames to be sent:")
no_frames_label.grid(column=0, row=2)

data_label = Label(window, text="Data to be transferred:")
data_label.grid(column=0, row=3)

# create entry fields
timeout_entry = Entry(window)
timeout_entry.grid(column=1, row=0)

sleep_entry = Entry(window)
sleep_entry.grid(column=1, row=1)

no_frames_entry = Entry(window)
no_frames_entry.grid(column=1, row=2)

data_entry = Entry(window)
data_entry.grid(column=1, row=3)

# create function to start sending on a separate thread
def start_send():
    # create sender thread
    sender_thread = threading.Thread(target=send, args=(
        float(timeout_entry.get()),
        float(sleep_entry.get()),
        int(no_frames_entry.get()),
        data_entry.get()
    ))

    # start sender thread
    sender_thread.start()

# create button to send data
send_button = Button(window, text="Send", command=start_send)
send_button.grid(column=1, row=4)

# create function to start receiving on a separate thread
def start_receive():
    # create receiver thread
    receiver_thread = threading.Thread(target=receive)

    # start receiver thread
    receiver_thread.start()

# create button to receive data
receive_button = Button(window, text="Receive", command=start_receive)
receive_button.grid(column=1, row=5)

# create function to stop sender and receiver threads
def stop_threads():
    # stop sender and receiver threads
    stop_sender()
    stop_receiver()

# create button to stop sender and receiver threads
stop_button = Button(window, text="Stop", command=stop_threads)
stop_button.grid(column=1, row=6)

# run the window
window.mainloop()