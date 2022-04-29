from be8bbbce.components.register import RegisterInOut
from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus


class InstructionRegister(RegisterInOut):
    def __init__(self,
                 signals: Signals,
                 bus: Bus,
                 address_length: int) -> None:
        super().__init__(signals, bus, Signals.INSTR_IN, Signals.INSTR_OUT)
        self.address_length = address_length
        self.max_plus_one = 1 << address_length

    def enable_out(self) -> None:
        # only send address to bus, not instruction
        self.bus.value = self.value % self.max_plus_one
