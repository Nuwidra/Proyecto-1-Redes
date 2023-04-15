import time
import random


class PhysicalLayer:
    def __init__(self, error_rate):
        self.error_rate = error_rate

    def send(self, frame):
        if random.random() > self.error_rate:
            return frame
        else:
            return None

    def receive(self):
        return b"Frame desde la capa física"


class NetworkLayer:
    def __init__(self, data):
        self.data = data

    def send(self):
        return self.data

    def receive(self, data):
        print("Capa de red recibió los datos:", data)


# Ejemplo de uso
def main():
    # Configuración de capa física
    error_rate = 0.3
    physical_layer = PhysicalLayer(error_rate)

    # Configuración de capa de red
    data = b"Datos desde la capa de red"
    network_layer = NetworkLayer(data)

    # Simulación de envío de datos
    while True:
        # Capa de red lista para enviar datos
        data = network_layer.send()

        # Capa física envía el frame
        frame = physical_layer.send(data)

        if frame is not None:
            # Frame llega sin errores a la capa de enlace
            event = FrameArrivalEvent(time.time(), frame)
            handle_event(event)
        else:
            # Frame llega con errores a la capa de enlace
            event = CksumErrEvent(time.time(), data)
            handle_event(event)


def handle_event(event):
    if event.type == "frame_arrival":
        print("Evento de llegada de frame sin errores a la capa de enlace:", event.data)
        # Realizar acción correspondiente
    elif event.type == "cksum_err":
        print("Evento de error de checksum en la capa física:", event.data)
        # Realizar acción correspondiente
    elif event.type == "timeout":
        print("Evento de timeout en el timer")
        # Realizar acción correspondiente
    elif event.type == "ack_timeout":
        print("Evento de timeout del ACK en el timer")
        # Realizar acción correspondiente
    elif event.type == "network_layer_ready":
        print("Evento de disponibilidad de dato en la capa de red:", event.data)
        network_layer.receive(event.data)  # Llamada a método de capa de red


main()
