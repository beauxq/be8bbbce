from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ count by 3 """
    computer.ram.memory[0] = a.m(ASM.LDI, 3)
    computer.ram.memory[1] = a.m(ASM.STA, 15)
    computer.ram.memory[2] = a.m(ASM.LDI, 0)
    computer.ram.memory[3] = a.m(ASM.ADD, 15)
    computer.ram.memory[4] = a.m(ASM.OUT, 0)
    computer.ram.memory[5] = a.m(ASM.JMP, 3)
