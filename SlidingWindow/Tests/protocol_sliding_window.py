import time
import random
import tkinter as tk

WINDOW_SIZE = 4
PACKET_DELAY = 1


class Packet:
    def __init__(self, data):
        self.data = data


class MockSlidingWindow:
    def __init__(self, packets):
        self.packets = packets
        self.window_start = 0
        self.window_end = min(WINDOW_SIZE, len(packets))
        self.unacknowledged_packets = set(range(self.window_start, self.window_end))

    def send_packet(self, packet_index):
        print(f"Sending packet {packet_index}: {self.packets[packet_index].data}")
        time.sleep(PACKET_DELAY)

    def receive_acknowledgment(self, ack_number):
        if ack_number in self.unacknowledged_packets:
            print(f"Received acknowledgment for packet {ack_number}")
            self.unacknowledged_packets.remove(ack_number)

    def slide_window(self):
        while self.window_start < len(self.packets):
            for i in self.unacknowledged_packets:
                self.send_packet(i)

            start_time = time.monotonic()
            while time.monotonic() - start_time < PACKET_DELAY:
                ack_number = self.simulate_packet_loss()
                if ack_number is not None:
                    self.receive_acknowledgment(ack_number)

            if not self.unacknowledged_packets:
                self.window_start = self.window_end
                self.window_end = min(self.window_end + WINDOW_SIZE, len(self.packets))
                self.unacknowledged_packets = set(range(self.window_start, self.window_end))
                print(f"Sliding window to packets {self.window_start} to {self.window_end}")
            else:
                print("Timeout waiting for acknowledgment, resending packets...")

    def simulate_packet_loss(self):
        if random.random() < 0.2:  # 20% packet loss rate
            return None
        else:
            return self.window_start


class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Sliding Window Protocol")

        self.packet_list = [Packet(f"Packet {i}") for i in range(10)]
        self.window = MockSlidingWindow(self.packet_list)

        self.current_packet_index = 0
        self.create_widgets()

    def create_widgets(self):
        self.packet_label = tk.Label(self.master, text=f"Current Packet: {self.current_packet_index}")
        self.packet_label.pack()

        self.send_packet_button = tk.Button(self.master, text="Send Packet", command=self.send_packet)
        self.send_packet_button.pack()

        #self.slide_window_button = tk.Button(self.master, text="Slide Window", command=self.slide_window)
        #self.slide_window_button.pack()

    def send_packet(self):
        if self.current_packet_index < len(self.packet_list):
            self.window.send_packet(self.current_packet_index)
            self.current_packet_index += 1
            self.packet_label.configure(text=f"Current Packet: {self.current_packet_index}")
        else:
            self.packet_label.configure(text="All packets sent!")

    def slide_window(self):
        self.window.slide_window()


root = tk.Tk()
app = Application(root)
root.mainloop()
