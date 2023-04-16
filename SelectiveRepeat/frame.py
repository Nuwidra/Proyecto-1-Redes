from enum import Enum
class Packet(Enum):
    data = 1
    ACK = 2
    CKSUM_ERR = 3
class Frame:
    packet = Packet
    sequenceNumber = 0
    confirmationNumber = 0
    packetInfo = ""

    def __init__(self, packet, sequenceNumber, confirmationNumber, packetInfo):
        self.packet = packet
        self.sequenceNumber = sequenceNumber
        self.confirmationNumber = confirmationNumber
        self.packetInfo = packetInfo