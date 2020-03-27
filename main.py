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

from asm import Assembler, ASM


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
    a = Assembler(4)

    computer = Computer()

    print(" add 28 + 14")
    computer.ram.memory[0] = a.m(ASM.LDA, 14)
    computer.ram.memory[1] = a.m(ASM.ADD, 15)
    computer.ram.memory[2] = a.m(ASM.OUT, 0)
    computer.ram.memory[3] = a.m(ASM.HLT, 0)
    computer.ram.memory[14] = 28
    computer.ram.memory[15] = 14

    computer.clock.go()

    computer.control.reset()

    print(" 5 + 6 - 7")
    computer.ram.memory[0] = a.m(ASM.LDA, 15)
    computer.ram.memory[1] = a.m(ASM.ADD, 14)
    computer.ram.memory[2] = a.m(ASM.SUB, 13)
    computer.ram.memory[3] = a.m(ASM.OUT, 0)
    computer.ram.memory[4] = a.m(ASM.HLT, 0)
    computer.ram.memory[13] = 7
    computer.ram.memory[14] = 6
    computer.ram.memory[15] = 5

    computer.clock.go()

    computer.control.reset()

    print(" count by 3")
    computer.ram.memory[0] = a.m(ASM.LDI, 3)
    computer.ram.memory[1] = a.m(ASM.STA, 15)
    computer.ram.memory[2] = a.m(ASM.LDI, 0)
    computer.ram.memory[3] = a.m(ASM.ADD, 15)
    computer.ram.memory[4] = a.m(ASM.OUT, 0)
    computer.ram.memory[5] = a.m(ASM.JMP, 3)

    computer.clock.go(200)

    computer.control.reset()

    print(" bounce between 0 and 256")
    computer.ram.memory[0] = a.m(ASM.OUT, 0)
    computer.ram.memory[1] = a.m(ASM.ADD, 15)
    computer.ram.memory[2] = a.m(ASM.JC, 4)
    computer.ram.memory[3] = a.m(ASM.JMP, 0)
    computer.ram.memory[4] = a.m(ASM.SUB, 15)
    computer.ram.memory[5] = a.m(ASM.OUT, 0)
    computer.ram.memory[6] = a.m(ASM.JZ, 0)
    computer.ram.memory[7] = a.m(ASM.JMP, 4)
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
    computer.ram.memory[0] = a.m(ASM.LDI, 0)
    computer.ram.memory[1] = a.m(ASM.STA, 15)
    computer.ram.memory[2] = a.m(ASM.LDI, 1)
    computer.ram.memory[3] = a.m(ASM.STA, 14)
    computer.ram.memory[4] = a.m(ASM.LDA, 7)
    computer.ram.memory[5] = a.m(ASM.SUB, 14)
    computer.ram.memory[6] = a.m(ASM.STA, 7)
    computer.ram.memory[7] = 7  # x = 7  interpreted as NOP/HLT
    computer.ram.memory[8] = a.m(ASM.LDA, 15)
    computer.ram.memory[9] = a.m(ASM.ADD, 13)
    computer.ram.memory[10] = a.m(ASM.STA, 15)
    computer.ram.memory[11] = a.m(ASM.OUT, 0)
    computer.ram.memory[12] = a.m(ASM.JMP, 4)
    computer.ram.memory[13] = 6  # y = 6

    computer.clock.go()

    computer.control.reset()

    print(" Ben Eater's multiplication")
    computer.ram.memory[0] = a.m(ASM.LDA, 14)
    computer.ram.memory[1] = a.m(ASM.SUB, 12)
    computer.ram.memory[2] = a.m(ASM.JC, 6)
    computer.ram.memory[3] = a.m(ASM.LDA, 13)
    computer.ram.memory[4] = a.m(ASM.OUT, 0)
    computer.ram.memory[5] = a.m(ASM.HLT, 0)
    computer.ram.memory[6] = a.m(ASM.STA, 14)
    computer.ram.memory[7] = a.m(ASM.LDA, 13)
    computer.ram.memory[8] = a.m(ASM.ADD, 15)
    computer.ram.memory[9] = a.m(ASM.STA, 13)
    computer.ram.memory[10] = a.m(ASM.JMP, 0)
    computer.ram.memory[11] = a.m(ASM.NOP, 0)
    computer.ram.memory[12] = 1
    computer.ram.memory[13] = 0  # product = 0
    computer.ram.memory[14] = 7  # x = 7
    computer.ram.memory[15] = 6  # y = 6

    computer.clock.go()

    computer.control.reset()

    print(" Ben Eater's fibonacci")
    computer.ram.memory[0] = a.m(ASM.LDI, 1)
    computer.ram.memory[1] = a.m(ASM.STA, 14)
    computer.ram.memory[2] = a.m(ASM.LDI, 0)
    computer.ram.memory[3] = a.m(ASM.OUT, 0)
    computer.ram.memory[4] = a.m(ASM.ADD, 14)
    computer.ram.memory[5] = a.m(ASM.STA, 15)
    computer.ram.memory[6] = a.m(ASM.LDA, 14)
    computer.ram.memory[7] = a.m(ASM.STA, 13)
    computer.ram.memory[8] = a.m(ASM.LDA, 15)
    computer.ram.memory[9] = a.m(ASM.STA, 14)
    computer.ram.memory[10] = a.m(ASM.LDA, 13)
    computer.ram.memory[11] = a.m(ASM.JC, 0)
    computer.ram.memory[12] = a.m(ASM.JMP, 3)

    computer.clock.go(2000)

    computer.control.reset()

    print(" jump indirect")
    computer.ram.memory[0] = a.m(ASM.LDI, 3)
    computer.ram.memory[1] = a.m(ASM.STA, 15)
    computer.ram.memory[2] = a.m(ASM.JMP, 10)
    computer.ram.memory[3] = a.m(ASM.LDI, 6)
    computer.ram.memory[4] = a.m(ASM.STA, 15)
    computer.ram.memory[5] = a.m(ASM.JMP, 10)
    computer.ram.memory[6] = a.m(ASM.LDI, 9)
    computer.ram.memory[7] = a.m(ASM.STA, 15)
    computer.ram.memory[8] = a.m(ASM.JMP, 10)
    computer.ram.memory[9] = a.m(ASM.HLT, 0)
    computer.ram.memory[10] = a.m(ASM.LDA, 15)
    computer.ram.memory[11] = a.m(ASM.OUT, 0)
    computer.ram.memory[12] = a.m(ASM.JI, 15)

    computer.clock.go()


if __name__ == "__main__":
    main()
