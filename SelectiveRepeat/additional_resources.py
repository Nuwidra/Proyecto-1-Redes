import pickle, random
from variables_sender import *
def shipping_confirmation():
    global actual_ack_seq_num
    socket_sender.bind(('', portA))
    while True:
        try:
            ack, _ = socket_sender.recvfrom(size_buffer)
            lock.acquire()
            ack_number = pickle.loads(ack)
            print("\nFrame Confirmed: ", ack_number)
            actual_ack_seq_num = ack_number
            frames_without_confirmation.remove(ack_number)
            lock.release()
        except Exception as e:
            print("Error: ", e)