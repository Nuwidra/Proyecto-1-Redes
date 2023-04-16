import socket               
from time import sleep
from threading import Timer
from random import random

sock = socket.socket()         # Crea un objeto del socket
host = socket.gethostname()  # Obtiene el nombre de la máquina
port = 8080                #reserva el puerto
sock.connect((host, port))
sock.setblocking(0)
data = list("0123456789abcdefghijklmnñopqrstuvwxyz")  # Datos a enviar



def timeout(i):  # Función timeout llama cuando el temporizador expira
    print("Timeout ", i)
    sock.send(str(i) + "," + data[i])  # Los dotos son reeviados
    timers[i] = Timer(5, timeout, args=[i], kwargs=dict())
    timers[i].start()  # Reinicia el temporizador

# Inicia la matriz del temporizador
timers = map(lambda t: Timer(3, timeout, args=[
             t], kwargs=dict()), range(0, len(data)))


# define receiver
def receiver():
    sl, su, sw = 0, 0, 4
    rcvd = [None] * len(data)
    while sl < len(data):
        try:
            if su < sl + sw and su < len(data):
                print("Enviando ", su)
                if random() < 0.8:
                    packet = Packet(su, data[su])
                    frame = Frame(packet, time.time())
                    sock.send(str(su) + "," + data[su])
                    timers[su] = frame
                else:
                    print("Frame ", su, " perdido en la transmisión")
                su += 1
            sleep(0.5)
            ack = sock.recv(1024)
            if ack is not None:
                ack_seq_num = int(ack.split(",")[0])
                print("ACK", ack_seq_num)
                if rcvd[ack_seq_num] is None:
                    rcvd[ack_seq_num] = Packet(ack_seq_num, None)
                if ack_seq_num >= sl and ack_seq_num < su:
                    rcvd[ack_seq_num] = Packet(ack_seq_num, None)
                    print("Temporizador cancelado ", ack_seq_num)
                    timers[ack_seq_num].cancel()
                    if ack_seq_num == sl:
                        while rcvd[sl] is not None:
                            sl += 1
                            print("SL se incrementa ", sl)
        except Exception as e:
            pass
    print("Data transmitida correctamente")
    sock.close()

receiver()
