import threading
import time
from GoBackNSender import sender
from GoBackNReceiver import receiver

# create sender and receiver threads
sender_thread = threading.Thread(target=sender)
receiver_thread = threading.Thread(target=receiver)

# start the threads
sender_thread.start()
receiver_thread.start()

# wait for the threads to finish
sender_thread.join()
receiver_thread.join()

print("Go-Back-N Protocol execution finished.")