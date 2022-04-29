from random import randrange
from be8bbbce.components.receiver import Receiver
from be8bbbce.components.register import RegisterIn
from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus


class _MemoryAddressRegister(RegisterIn):
    def __init__(self, signals: Signals, bus: Bus, address_length: int) -> None:
        super().__init__(signals, bus, Signals.MAR_IN)
        self.address_length = address_length
        self.address_count = 1 << self.address_length

    def load_in(self) -> None:
        self._value = self.bus.value % self.address_count


class Ram(Receiver):
    def __init__(self,
                 signals: Signals,
                 bus: Bus,
                 address_length: int,
                 bit_count: int,
                 clean_memory: bool) -> None:
        signals.listen(self)
        self.bus = bus
        self.mar = _MemoryAddressRegister(signals, bus, address_length)
        if clean_memory:
            self.memory = [0 for _ in range(self.mar.address_count)]
        else:  # random memory
            value_range = 1 << bit_count
            self.memory = [randrange(value_range)
                           for _ in range(self.mar.address_count)]
        self.ram_in = 0

    def receive_signal(self, code: str, value: int) -> None:
        if (code == Signals.CLOCK) and value:
            if self.ram_in:
                self.memory[self.mar.value] = self.bus.value
        elif code == Signals.RAM_IN:
            self.ram_in = value
        elif (code == Signals.RAM_OUT) and value:
            self.bus.value = self.memory[self.mar.value]
