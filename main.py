from signals import Signals
from clock import Clock
from register import RegisterInOut
from bus import Bus
from alu import ALU
from ram import Ram
from programcounter import ProgramCounter
from output import Output


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
        self.reg_a = RegisterInOut(self.signals, self.bus,
                                   Signals.REG_A_IN, Signals.REG_A_OUT)
        self.reg_b = RegisterInOut(self.signals, self.bus,
                                   Signals.REG_B_IN, Signals.REG_B_OUT)
        self.alu = ALU(self.signals, self.bus,
                       self.reg_a, self.reg_b, BIT_COUNT)
        self.ram = Ram(self.signals, self.bus, ADDRESS_LENGTH)
        self.pc = ProgramCounter(self.signals, self.bus, ADDRESS_LENGTH)
        self.out = Output(self.signals, self.bus, BIT_COUNT)


def main():
    computer = Computer()
    computer.clock.go_high()
    computer.clock.go_low()


if __name__ == "__main__":
    main()
