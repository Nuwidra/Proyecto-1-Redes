"""
A sliding window frame that can receive packets and deliver data.
"""

class Frame:
    """
    A sliding window frame that can receive packets and deliver data.
    """
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = [None] * window_size
        self.expected_seq_num = 0
        self.recv_base = 0

    def receive_packet(self, packet):
        """
        Receive a packet and return an acknowledgment packet.
        :param packet:
        :return: an acknowledgment packet
        """
        if packet.seq_num >= self.expected_seq_num and packet.seq_num < self.expected_seq_num + self.window_size:
            if self.window[packet.seq_num % self.window_size] is None:
                self.window[packet.seq_num % self.window_size] = packet
            if packet.seq_num == self.expected_seq_num:
                self._deliver_packets()
        return self._ack_packet(packet.seq_num)

    def _ack_packet(self, seq_num):
        """
        Create an acknowledgment packet for the given sequence number.
        :param seq_num:
        :return:  an acknowledgment packet
        """
        ack_num = seq_num + 1
        return Packet(ack_num, b'')

    def _deliver_packets(self):
        """
        Deliver packets to the application layer.
        :return: None
        """
        while self.window[self.recv_base % self.window_size] is not None:
            packet = self.window[self.recv_base % self.window_size]
            self.window[self.recv_base % self.window_size] = None
            self.recv_base += 1
            self.expected_seq_num += 1
            self._process_data(packet)

    def _process_data(self, packet):
        """
        Process the data in the given packet.
        :param packet:
        :return:
        """
        print(packet.data.decode('utf-8'))

class Packet:
    """"
    A packet that can be sent over a network.
    """
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data