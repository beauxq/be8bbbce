from components.register import RegisterIn
from components.signals import Signals
from components.alu import ALU


class Flags(RegisterIn):
    def __init__(self, signals: Signals, alu: ALU):
        super().__init__(signals, alu, Signals.FLAGS_IN)
        # duck typing - a bus just needs to have a "value" attribute
        # ALU has a "value" attribute
        self.alu = alu  # bus also references the same object

    def load_in(self):
        self.value = (self.alu.carry << 1) + (self.alu.value == 0)

    def get_carry(self):
        return self.value >> 1

    def get_zero(self):
        return self.value % 2
