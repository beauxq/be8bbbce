from signals import Signals
from clock import Clock
from register import Register
from bus import Bus
from alu import ALU
from ram import Ram


INSTRUCTION_LENGTH = 4
ADDRESS_LENGTH = 4
# One word can contain an instruction and an address.
BIT_COUNT = INSTRUCTION_LENGTH + ADDRESS_LENGTH

# Some modules (registers, bus) don't need to know how many bits,
# because they just use the Python int data structure for their values.
# The ALU needs to know how many bits so it can emulate overflow accurately.


class Computer():
    def __init__(self):
        self.signals = Signals()
        self.clock = Clock(self.signals)
        self.bus = Bus()
        self.reg_a = Register(self.signals, self.bus,
                              Signals.REG_A_IN, Signals.REG_A_OUT)
        self.reg_b = Register(self.signals, self.bus,
                              Signals.REG_B_IN, Signals.REG_B_OUT)
        self.alu = ALU(self.signals, self.bus,
                       self.reg_a, self.reg_b, BIT_COUNT)
        self.ram = Ram(self.signals, self.bus, ADDRESS_LENGTH)


def main():
    computer = Computer()
    computer.clock.go_high()
    computer.clock.go_low()


if __name__ == "__main__":
    main()
