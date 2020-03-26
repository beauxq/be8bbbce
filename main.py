from signals import Signals
from clock import Clock
from register import RegisterInOut
from bus import Bus
from alu import ALU
from ram import Ram
from programcounter import ProgramCounter
from output import Output
from instructionregister import InstructionRegister
from flags import Flags
from control import Control


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
        self.ir = InstructionRegister(self.signals, self.bus, ADDRESS_LENGTH)
        self.flags = Flags(self.signals, self.alu)
        self.control = Control(self.signals, self.ir, self.flags)


def main():
    computer = Computer()

    print(" add 28 + 14")
    computer.ram.memory[0] = 0b00011110  # LDA 14
    computer.ram.memory[1] = 0b00101111  # ADD 15
    computer.ram.memory[2] = 0b11100000  # OUT
    computer.ram.memory[3] = 0b11110000  # HLT
    computer.ram.memory[0b1110] = 28
    computer.ram.memory[0b1111] = 14

    computer.clock.go()

    computer.control.reset()

    print(" 5 + 6 - 7")
    computer.ram.memory[0] = 0b00011111  # LDA 15
    computer.ram.memory[1] = 0b00101110  # ADD 14
    computer.ram.memory[2] = 0b00111101  # SUB 13
    computer.ram.memory[3] = 0b11100000  # OUT
    computer.ram.memory[4] = 0b11110000  # HLT
    computer.ram.memory[13] = 7
    computer.ram.memory[14] = 6
    computer.ram.memory[15] = 5

    computer.clock.go()

    computer.control.reset()

    print(" count by 3")
    computer.ram.memory[0] = 0b01010011  # LDI 3
    computer.ram.memory[1] = 0b01001111  # STA 15
    computer.ram.memory[2] = 0b01010000  # LDI 0
    computer.ram.memory[3] = 0b00101111  # ADD 15
    computer.ram.memory[4] = 0b11100000  # OUT
    computer.ram.memory[5] = 0b01100011  # JMP 3

    computer.clock.go(200)

    computer.control.reset()

    print(" bounce between 0 and 256")
    computer.ram.memory[0] = 0b11100000  # OUT
    computer.ram.memory[1] = 0b00101111  # ADD 15
    computer.ram.memory[2] = 0b01110100  # JC 4
    computer.ram.memory[3] = 0b01100000  # JMP 0
    computer.ram.memory[4] = 0b00111111  # SUB 15
    computer.ram.memory[5] = 0b11100000  # OUT
    computer.ram.memory[6] = 0b10000000  # JZ 0
    computer.ram.memory[7] = 0b01100100  # JMP 4
    computer.ram.memory[15] = 32

    computer.clock.go(400)

    computer.control.reset()

    print(" Matthew Kudzin multiply with no conditional jump")
    """
    0:   LDI   0
1:    STA  15
2:    LDI    1
3:    STA   14
4:    LDA   7
5:    SUB   14
6:    STA    7
7:     <x>
8:    LDA   15
9:    ADD   13
10:  STA   15
11:   OUT
12:  JMP   4
13:  <y>
    """
    computer.ram.memory[0] = 0b01010000  # LDI 0
    computer.ram.memory[1] = 0b01001111  # STA 15
    computer.ram.memory[2] = 0b01010001  # LDI 1
    computer.ram.memory[3] = 0b01001110  # STA 14
    computer.ram.memory[4] = 0b00010111  # LDA 7
    computer.ram.memory[5] = 0b00111110  # SUB 14
    computer.ram.memory[6] = 0b01000111  # STA 7
    computer.ram.memory[7] = 0b00000111  # x = 7  interpreted as NOP/HLT
    computer.ram.memory[8] = 0b00011111  # LDA 15
    computer.ram.memory[9] = 0b00101101  # ADD 13
    computer.ram.memory[10] = 0b01001111  # STA 15
    computer.ram.memory[11] = 0b11100000  # OUT
    computer.ram.memory[12] = 0b01100100  # JMP 4
    computer.ram.memory[13] = 0b00000110  # y = 6

    computer.clock.go()

    computer.control.reset()

    print(" Ben Eater's multiplication")
    computer.ram.memory[0] = 0b00011110  # LDA 14
    computer.ram.memory[1] = 0b00111100  # SUB 12
    computer.ram.memory[2] = 0b01110110  # JC  6
    computer.ram.memory[3] = 0b00011101  # LDA 13
    computer.ram.memory[4] = 0b11100000  # OUT
    computer.ram.memory[5] = 0b11110000  # HLT
    computer.ram.memory[6] = 0b01001110  # STA 14
    computer.ram.memory[7] = 0b00011101  # LDA 13
    computer.ram.memory[8] = 0b00101111  # ADD 15
    computer.ram.memory[9] = 0b01001101  # STA 13
    computer.ram.memory[10] = 0b01100000  # JMP 0
    computer.ram.memory[11] = 0b00000000  # NOP
    computer.ram.memory[12] = 0b00000001  # 1
    computer.ram.memory[13] = 0b00000000  # product = 0
    computer.ram.memory[14] = 0b00000111  # x = 7
    computer.ram.memory[15] = 0b00000110  # y = 6

    computer.clock.go()

    computer.control.reset()

    print(" Ben Eater's fibonacci")
    computer.ram.memory[0] = 0b01010001  # LDI 1
    computer.ram.memory[1] = 0b01001110  # STA 14
    computer.ram.memory[2] = 0b01010000  # LDI 0
    computer.ram.memory[3] = 0b11100000  # OUT
    computer.ram.memory[4] = 0b00101110  # ADD 14
    computer.ram.memory[5] = 0b01001111  # STA 15
    computer.ram.memory[6] = 0b00011110  # LDA 14
    computer.ram.memory[7] = 0b01001101  # STA 13
    computer.ram.memory[8] = 0b00011111  # LDA 15
    computer.ram.memory[9] = 0b01001110  # STA 14
    computer.ram.memory[10] = 0b00011101  # LDA 13
    computer.ram.memory[11] = 0b01110000  # JC  0
    computer.ram.memory[12] = 0b01100011  # JMP 3
    computer.ram.memory[13] = 0b00000000  # 0
    computer.ram.memory[14] = 0b00000000  # 0
    computer.ram.memory[15] = 0b00000000  # 0

    computer.clock.go(2000)

    computer.control.reset()

    print(" jump indirect")
    computer.ram.memory[0] = 0b01010011  # LDI 3
    computer.ram.memory[1] = 0b01001111  # STA 15
    computer.ram.memory[2] = 0b01101010  # JMP 10
    computer.ram.memory[3] = 0b01010110  # LDI 6
    computer.ram.memory[4] = 0b01001111  # STA 15
    computer.ram.memory[5] = 0b01101010  # JMP 10
    computer.ram.memory[6] = 0b01011001  # LDI 9
    computer.ram.memory[7] = 0b01001111  # STA 15
    computer.ram.memory[8] = 0b01101010  # JMP 10
    computer.ram.memory[9] = 0b11110000  # HLT
    computer.ram.memory[10] = 0b00011111  # LDA 15
    computer.ram.memory[11] = 0b11100000  # OUT
    computer.ram.memory[12] = 0b10011111  # JI 15

    computer.clock.go()


if __name__ == "__main__":
    main()
