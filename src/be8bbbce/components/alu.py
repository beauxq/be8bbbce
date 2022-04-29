from be8bbbce.components.bus import Bus
from be8bbbce.components.register import RegisterOut, Register
from be8bbbce.components.signals import Signals


class ALU(RegisterOut):
    def __init__(self,
                 signals: Signals,
                 bus: Bus,
                 reg_a: Register,
                 reg_b: Register,
                 bit_count: int):
        super().__init__(signals, bus, Signals.ALU_OUT)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.max_plus_one = 1 << bit_count
        self.bit_count = bit_count
        self.carry = 0
        self.subtract = 0
        self.enabled = 0  # output to bus

    def twos_complement_negation(self, x: int) -> int:
        assert 0 <= x < self.max_plus_one
        return (self.max_plus_one - x) % self.max_plus_one

    def add(self) -> None:
        # Register a and register b are unsigned integers.
        # The computer uses 2's complement to subtract, but only to subtract.
        # Nothing is ever interpreted in 2's complement.
        reg_b_value = self.reg_b.value
        if self.subtract:
            reg_b_value = self.twos_complement_negation(reg_b_value)
        self.value = self.reg_a.value + reg_b_value
        self.carry = 0
        if self.value >= self.max_plus_one:
            self.value %= self.max_plus_one
            self.carry = 1

        if self.enabled:
            # put result on bus again
            super().receive_signal(Signals.ALU_OUT, 1)

    def receive_signal(self, code: str, value: int) -> None:
        super().receive_signal(code, value)
        if (code == Signals.CLOCK) and (not value):
            # in original computer, this is happening
            # constantly all the time and needs no signal
            self.add()
        elif code == Signals.SUBTRACT:
            self.subtract = value
            self.add()
        elif code == Signals.ALU_OUT:
            self.enabled = value
