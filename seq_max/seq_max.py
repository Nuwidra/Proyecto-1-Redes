import math

# Definir el número máximo de secuencia predeterminado
DEFAULT_MAX_SEQ = 7

class Protocol:
    def __init__(self, max_seq=DEFAULT_MAX_SEQ):
        self.max_seq = max_seq

    def send(self, data):
        # Implementar la lógica de envío de datos
        pass

    def receive(self):
        # Implementar la lógica de recepción de datos
        pass

    def set_max_seq(self, max_seq):
        # Verificar que el número máximo de secuencia esté dentro del rango adecuado
        max_seq = min(max_seq, int(math.pow(2, math.ceil(math.log2(max_seq + 1))) - 1))
        self.max_seq = max_seq

# Ejemplo de uso
p = Protocol()
print("Número máximo de secuencia predeterminado:", p.max_seq)

max_seq = int(input("Ingrese el número máximo de secuencia: "))
p.set_max_seq(max_seq)
print("Número máximo de secuencia actualizado:", p.max_seq)
