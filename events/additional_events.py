import time
import random


class Event:
    def __init__(self, time, event_type, data=None):
        self.time = time
        self.type = event_type
        self.data = data

    def __lt__(self, other):
        return self.time < other.time


class FrameArrivalEvent(Event):
    def __init__(self, time, frame):
        super().__init__(time, "frame_arrival", frame)


class CksumErrEvent(Event):
    def __init__(self, time, frame):
        super().__init__(time, "cksum_err", frame)


class TimeoutEvent(Event):
    def __init__(self, time):
        super().__init__(time, "timeout")


class AckTimeoutEvent(Event):
    def __init__(self, time):
        super().__init__(time, "ack_timeout")


class NetworkLayerReadyEvent(Event):
    def __init__(self, time, data):
        super().__init__(time, "network_layer_ready", data)


# Ejemplo de uso
def generar_eventos():
    # Generar eventos aleatorios
    eventos = []
    eventos.append(FrameArrivalEvent(time.time() + 2.0, b"Frame sin errores"))
    eventos.append(CksumErrEvent(time.time() + 3.0, b"Frame con errores"))
    eventos.append(TimeoutEvent(time.time() + 4.0))
    eventos.append(AckTimeoutEvent(time.time() + 5.0))
    eventos.append(NetworkLayerReadyEvent(time.time() + 1.0, b"Dato a enviar"))

    # Ordenar eventos por tiempo
    eventos.sort()

    return eventos


eventos = generar_eventos()

# Simulación de eventos
for evento in eventos:
    if evento.type == "frame_arrival":
        print("Evento de llegada de frame sin errores a la capa de enlace:", evento.data)
    elif evento.type == "cksum_err":
        print("Evento de error de checksum en la capa física:", evento.data)
    elif evento.type == "timeout":
        print("Evento de timeout en el timer")
    elif evento.type == "ack_timeout":
        print("Evento de timeout del ACK en el timer")
    elif evento.type == "network_layer_ready":
        print("Evento de disponibilidad de dato en la capa de red:", evento.data)
