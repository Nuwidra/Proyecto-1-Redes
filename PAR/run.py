
import threading
from PAR.PARReceiver import receive_data, stop_receiver
from PAR.PARSender import send_data, stop_sender

# Define the data to be sent
data = "Hello, world!"
frame = 5

# Start receiver in a separate thread
receiver_thread = threading.Thread(target=receive_data)
receiver_thread.start()

# Start sender
sender_thread = threading.Thread(target=send_data, args=(frame, data))
sender_thread.start()

# Wait for sender to finish
sender_thread.join()

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


