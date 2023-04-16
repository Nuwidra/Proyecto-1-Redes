import socket
total_size = 8192
frame_size = 0
frame_list = []
expected_seq_num = 0
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
portA = 4004
portB = 4006
receiver_socket.bind(('', portB))