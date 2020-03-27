from components.receiver import Receiver
from components.register import RegisterIn
from components.signals import Signals
from components.bus import Bus
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

    def receive_signal(self, code: str, value: int):
        if (code == Signals.CLOCK) and value:
            if self.ram_in:
                self.memory[self.mar.value] = self.bus.value
        elif code == Signals.RAM_IN:
            self.ram_in = value
        elif (code == Signals.RAM_OUT) and value:
            self.bus.value = self.memory[self.mar.value]
