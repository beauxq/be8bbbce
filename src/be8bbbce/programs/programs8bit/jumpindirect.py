from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ jump indirect """
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
