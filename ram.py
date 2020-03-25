from receiver import Receiver
from register import RegisterIn
from signals import Signals
from bus import Bus
from typing import List


class _MemoryAddressRegister(RegisterIn):
    def __init__(self, signals: Signals, bus: Bus, address_length: int):
        super().__init__(signals, bus, Signals.MAR_IN)
        self.address_length = address_length
        self.address_count = 1 << self.address_length

    def load_in(self):
        self.value = self.bus.value % self.address_count


class Ram(Receiver):
    def __init__(self, signals: Signals, bus: Bus, address_length: int):
        signals.listen(self)
        self.bus = bus
        self.mar = _MemoryAddressRegister(signals, bus, address_length)
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
