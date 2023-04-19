import time
import random

# Physical layer events are objects that are used to simulate the arrival of events in the simulation.
class PhysicalLayer:
    def __init__(self, error_rate):
        self.error_rate = error_rate
    # send() method simulates the sending of a frame to the physical layer.
    def send(self, frame):
        if random.random() > self.error_rate:
            return frame
        else:
            return None
    # receive() method simulates the reception of a frame from the physical layer.
    def receive(self):
        return b"Frame desde la capa física"

# Network layer events are objects that are used to simulate the arrival of events in the simulation.
class NetworkLayer:
    # The data attribute is the data to be sent.
    def __init__(self, data):
        self.data = data
    # send() method simulates the sending of data to the network layer.
    def send(self):
        return self.data
    # receive() method simulates the reception of data from the network layer.
    def receive(self, data):
        print("Capa de red recibió los datos:", data)


# Main function of the simulator
def main():
    # Configuración de capa física
    error_rate = 0.3
    physical_layer = PhysicalLayer(error_rate)

    # Configuration of network layer
    data = b"Datos desde la capa de red"
    network_layer = NetworkLayer(data)

    # Simulation loop
    while True:
        # Layer network sends data
        data = network_layer.send()

        # Layer physical receives data
        frame = physical_layer.send(data)

        if frame is not None:
            # FrameArrivalEvent is an event that simulates the arrival of a frame to the link layer.
            event = FrameArrivalEvent(time.time(), frame)
            handle_event(event)
        else:
            # CksumErrEvent is an event that simulates the arrival of a frame with checksum error to the link layer.
            event = CksumErrEvent(time.time(), data)
            handle_event(event)

# Events are objects that are used to simulate the arrival of events in the simulation.
def handle_event(event):
    if event.type == "frame_arrival":
        print("Evento de llegada de frame sin errores a la capa de enlace:", event.data)
    elif event.type == "cksum_err":
        print("Evento de error de checksum en la capa física:", event.data)
    elif event.type == "timeout":
        print("Evento de timeout en el timer")
    elif event.type == "ack_timeout":
        print("Evento de timeout del ACK en el timer")
    elif event.type == "network_layer_ready":
        print("Evento de disponibilidad de dato en la capa de red:", event.data)
        network_layer.receive(event.data)  # Llamada a método de capa de red


main()
