from enum import Enum
# Packet class is used to create a packet.
class Packet(Enum):
    # data is used to store the data.
    data = 1
    # type is used to store the type of the packet.
    ACK = 2
    # checksum is used to store the checksum of the packet.
    CKSUM_ERR = 3

# Frame class is used to create a frame.
class Frame:
    # packet is used to store the packet.
    packet = Packet
    # sequenceNumber is used to store the sequence number of the frame.
    sequenceNumber = 0
    # confirmationNumber is used to store the confirmation number of the frame.
    confirmationNumber = 0
    # packetInfo is used to store the packet info.
    packetInfo = ""

    # __init__ function is used to initialize the frame.
    def __init__(self, packet, sequenceNumber, confirmationNumber, packetInfo):
        self.packet = packet
        self.sequenceNumber = sequenceNumber
        self.confirmationNumber = confirmationNumber
        self.packetInfo = packetInfo