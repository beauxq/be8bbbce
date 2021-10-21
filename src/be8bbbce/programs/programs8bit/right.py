from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ pseudo- bit shift right """
    computer.ram.memory[0] = a.m(ASM.LDA, 9)
    computer.ram.memory[1] = a.m(ASM.LDA, 10)
    computer.ram.memory[2] = a.m(ASM.LDA, 11)
    computer.ram.memory[3] = a.m(ASM.LDA, 12)
    computer.ram.memory[4] = a.m(ASM.LDI, 8)
    computer.ram.memory[5] = a.m(ASM.LDI, 4)
    computer.ram.memory[6] = a.m(ASM.LDI, 2)
    computer.ram.memory[7] = a.m(ASM.LDI, 1)
    computer.ram.memory[8] = a.m(ASM.JMP, 0)
    computer.ram.memory[9] = 128
    computer.ram.memory[10] = 64
    computer.ram.memory[11] = 32
    computer.ram.memory[12] = 16
