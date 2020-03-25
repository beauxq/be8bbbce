from signals import Signals
from clock import Clock
from register import Register
from bus import Bus
from alu import ALU


BIT_COUNT = 8
# Some modules (registers, bus) don't need to know how many bits,
# because they just use the Python int data structure for their values.
# The ALU needs to know how many bits so it can emulate overflow accurately.


class Computer():
    def __init__(self):
        self.signals = Signals()
        self.clock = Clock(self.signals)
        self.bus = Bus()
        self.reg_a = Register(self.signals, self.bus, "a_in", "a_out")
        self.reg_b = Register(self.signals, self.bus, "b_in", "b_out")
        self.alu = ALU(self.bus, self.signals,
                       self.reg_a, self.reg_b, BIT_COUNT)


def main():
    computer = Computer()
    computer.clock.go_high()
    computer.clock.go_low()


if __name__ == "__main__":
    main()
