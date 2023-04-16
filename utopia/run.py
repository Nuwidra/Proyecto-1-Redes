from threading import Thread
from UtopiaSender import send, stop as stop_sender
from UtopiaReceiver import receive, stop as stop_receiver

# Modify these values as desired
TIMEOUT_INTERVAL = 0.5
SLEEP_INTERVAL = 0.05
NO_OF_FRAMES = 3
DATA = "Hello, Utopia!"

# Start receiver in a separate thread
receiver_thread = Thread(target=receive)
receiver_thread.start()

# Start sender
send_thread = Thread(target=send, args=(TIMEOUT_INTERVAL, SLEEP_INTERVAL, NO_OF_FRAMES, DATA))
send_thread.start()

# Wait for sender to finish
send_thread.join()

# Stop the receiver with error handling oserror if the socket is already closed by the sender
try:
    stop_receiver()
except OSError:
    pass

# Stop the sender with error handling oserror if the socket is already closed by the receiver
try:
    stop_sender()
except OSError:
    pass

# Wait for receiver to finish
receiver_thread.join()



