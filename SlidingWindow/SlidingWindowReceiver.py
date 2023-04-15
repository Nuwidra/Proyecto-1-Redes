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
    sl, su, sw = 0, 0, 4  # su:frame sl:contador
    rcvd = [False] * len(data)  # Matriz para almacenar si se ha recibido una trama con los datos
    while sl < len(data):
        try:
            if su < sl + sw and su < len(data):
                print("Enviando ", su)
                # Solo 80%  de la solicitudes es reenviado, esto para tener el canal con ruido
                if random() < 0.8:
                    sock.send(str(su) + "," + data[su])
                else:
                    print("Frame ", su, " perdido en la transmisión")
                timers[su].start()
                su += 1
            sleep(0.5)
            ack = sock.recv(1024)
            if ack is not None:
                ack = int(ack.split(",")[0])
                print("ACK", ack)
                if ack >= sl and ack < su:  # Comprobar la validez de ACK (acknowledgemen o acuse de recibo)
                    rcvd[ack] = True
                    print("Temporizador cancelado ", ack)
                    timers[ack].cancel()  # Cancela el temporizador
                    if ack == sl:
                        while rcvd[sl]:  # Incrementa el SL
                            sl += 1
                            print("SL se incrementa ", sl)
        except Exception as e:
            pass
    print("Data transmitida correctamente")
    sock.close()

receiver()
