import threading

from SelectiveRepeat.sender import sender, stop_sender
from SelectiveRepeat.receiver import receiver, stop_receiver

if __name__ == '__main__':
    # Message to send
    data = "Hello world!"
    # Start receiver in a separate thread
    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.start()

    # Start sender
    sender_thread = threading.Thread(target=sender, args=(data,))
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

