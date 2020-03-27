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
ADDRESS_LENGTH = 12
BIT_COUNT = INSTRUCTION_LENGTH + ADDRESS_LENGTH


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
    a = Assembler(12)

    computer = Computer()

    print(" multiply subroutine")
    multiply_subroutine = [
        a.m(ASM.LDA, 2033),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC, 2004),
        a.m(ASM.JMP, 2010),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2033),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2034),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 0),
        a.m(ASM.STA, 2036),
        a.m(ASM.LDI, 0),
        a.m(ASM.ADD, 2033),
        a.m(ASM.JZ, 2022),
        a.m(ASM.LDA, 2036),
        a.m(ASM.ADD, 2034),
        a.m(ASM.STA, 2036),
        a.m(ASM.LDA, 2033),
        a.m(ASM.SUB, 4001),
        a.m(ASM.STA, 2033),
        a.m(ASM.JMP, 2012),
        a.m(ASM.JI, 2035)
    ]
    """
    2033 a operand
    2034 b operand
    2035 pc return location
    2036 result location
    """

    computer.ram.memory[0] = a.m(ASM.LDI, 7)
    computer.ram.memory[1] = a.m(ASM.STA, 2033)  # a operand
    computer.ram.memory[2] = a.m(ASM.LDI, 6)
    computer.ram.memory[3] = a.m(ASM.STA, 2034)  # b operand
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2035)  # return program counter
    computer.ram.memory[6] = a.m(ASM.JMP, 2000)  # multiply subroutine
    computer.ram.memory[7] = a.m(ASM.LDA, 2036)  # result
    computer.ram.memory[8] = a.m(ASM.OUT, 0)
    computer.ram.memory[9] = a.m(ASM.HLT, 0)

    address = 2000
    for instruction in multiply_subroutine:
        computer.ram.memory[address] = instruction
        address += 1

    computer.ram.memory[4000] = 1 << (BIT_COUNT - 1)  # min signed
    computer.ram.memory[4001] = 1

    computer.clock.go(1000)


if __name__ == "__main__":
    main()
