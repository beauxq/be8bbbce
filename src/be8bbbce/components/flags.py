from be8bbbce.components.register import RegisterIn
from be8bbbce.components.signals import Signals
from be8bbbce.components.alu import ALU


class Flags(RegisterIn):
    def __init__(self, signals: Signals, alu: ALU) -> None:
        super().__init__(signals, alu, Signals.FLAGS_IN)
        # duck typing - a bus just needs to have a "value" attribute
        # ALU has a "value" attribute
        self.alu = alu  # bus also references the same object

    def load_in(self) -> None:
        self._value = (self.alu.carry << 1) + (self.alu.value == 0)

    def get_carry(self) -> int:
        return self._value >> 1

    def get_zero(self) -> int:
        return self._value % 2
