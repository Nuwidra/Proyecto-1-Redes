import threading, socket
from SelectiveRepeat.frame import Kind
counter_window = 0
size_buffer = 1024
frames_without_confirmation = []
frames_window = []
attempts = 0
actual_seq_num = 0
actual_ack_seq_num = -1
lock = threading.Lock()
network_layer_flag = True
frame_type = [Kind.DATA,
              Kind.CKSUM_ERR]
socket_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
portA = 4004
portB = 4006