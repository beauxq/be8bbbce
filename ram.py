from receiver import Receiver
from signals import Signals
from bus import Bus
from typing import List


class _MemoryAddressRegister(Receiver):
    def __init__(self, signals: Signals, bus: Bus, bit_count: int):
        signals.listen(self)
        self.bus = bus
        self.address_length = bit_count - 4  # 4 bits for instructions
        self.address_count = 2 ** self.address_length
        self.mar_in = 0
        self.value = 0

    def receive_signal(self, code: str, value: int):
        if code == Signals.CLOCK and value == 1:
            if self.mar_in:
                self.value = self.bus.value % self.address_count
        elif code == Signals.MAR_IN:
            self.mar_in = value


class Ram(Receiver):
    def __init__(self, signals: Signals, bus: Bus, bit_count: int):
        signals.listen(self)
        self.bus = bus
        self.mar = _MemoryAddressRegister(signals, bus, bit_count)
        self.memory: List[int] = [0 for _ in range(self.mar.address_count)]
        self.ram_in = 0
        self.ram_out = 0

    def receive_signal(self, code: str, value: int):
        if code == Signals.CLOCK and value == 1:
            if self.ram_in and self.ram_out:
                raise ValueError("I don't know what should happen if "
                                 "in and out at the same time.")
            if self.ram_in:
                self.memory[self.mar.value] = self.bus.value
            if self.ram_out:
                self.bus.value = self.memory[self.mar.value]
        elif code == Signals.RAM_IN:
            self.ram_in = value
        elif code == Signals.RAM_OUT:
            self.ram_out = value
