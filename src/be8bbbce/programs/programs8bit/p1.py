from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ add 28 + 14 """
    computer.ram.memory[0] = a.m(ASM.LDA, 14)
    computer.ram.memory[1] = a.m(ASM.ADD, 15)
    computer.ram.memory[2] = a.m(ASM.OUT, 0)
    computer.ram.memory[3] = a.m(ASM.HLT, 0)
    computer.ram.memory[14] = 28
    computer.ram.memory[15] = 14
