from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ 5 + 6 - 7 """
    computer.ram.memory[0] = a.m(ASM.LDA, 15)
    computer.ram.memory[1] = a.m(ASM.ADD, 14)
    computer.ram.memory[2] = a.m(ASM.SUB, 13)
    computer.ram.memory[3] = a.m(ASM.OUT, 0)
    computer.ram.memory[4] = a.m(ASM.HLT, 0)
    computer.ram.memory[13] = 7
    computer.ram.memory[14] = 6
    computer.ram.memory[15] = 5
