from tkinter import *
from threading import Thread
from GoBackNSender import sender
from GoBackNReceiver import receiver, stop_receiver
from events.events import disable_network_layer

# create a window
window = Tk()

# set the title
window.title("Go Back N Protocol")

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

# create button to send data
send_button = Button(window, text="Send", command=lambda: sender())
send_button.grid(column=1, row=4)

# create button to receive data
receive_button = Button(window, text="Receive", command=lambda: Thread(target=receiver).start())
receive_button.grid(column=1, row=5)

# create button to stop sender and receiver
stop_button = Button(window, text="Stop", command=lambda: [disable_network_layer(), stop_receiver()])
stop_button.grid(column=1, row=6)

# create button to pause sending
pause_button = Button(window, text="Pause")
pause_button.grid(column=1, row=7)

# run the window
window.mainloop()