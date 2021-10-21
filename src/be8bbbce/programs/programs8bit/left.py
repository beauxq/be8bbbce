from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ bit shift left """
    computer.ram.memory[0] = a.m(ASM.LDI, 1)
    computer.ram.memory[1] = a.m(ASM.STA, 15)
    computer.ram.memory[2] = a.m(ASM.LDA, 15)
    computer.ram.memory[3] = a.m(ASM.ADD, 15)
    computer.ram.memory[4] = a.m(ASM.STA, 15)
    computer.ram.memory[5] = a.m(ASM.JC, 0)
    computer.ram.memory[6] = a.m(ASM.JMP, 2)
