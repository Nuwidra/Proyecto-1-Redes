import threading
from StopNWaitReceiver import receive, stop_receiver
from StopNWaitsender import send, stop_sender

# define parameters
TIMEOUT_INTERVAL = 5
SLEEP_INTERVAL = 1
no_of_frames = 10
data = "Hello World"

# create sender and receiver threads
sender_thread = threading.Thread(target=send, args=(TIMEOUT_INTERVAL, SLEEP_INTERVAL, no_of_frames, data))
receiver_thread = threading.Thread(target=receive)

# start threads
sender_thread.start()
receiver_thread.start()

# wait for threads to finish
sender_thread.join()
receiver_thread.join()

# close sockets
sender_thread = threading.Thread(target=stop_sender)
receiver_thread = threading.Thread(target=stop_receiver)
