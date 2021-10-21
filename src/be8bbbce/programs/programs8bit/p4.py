from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ bounce between 0 and 256 - address 15 holds step size """
    computer.ram.memory[0] = a.m(ASM.OUT, 0)
    computer.ram.memory[1] = a.m(ASM.ADD, 15)
    computer.ram.memory[2] = a.m(ASM.JC, 4)
    computer.ram.memory[3] = a.m(ASM.JMP, 0)
    computer.ram.memory[4] = a.m(ASM.SUB, 15)
    computer.ram.memory[5] = a.m(ASM.OUT, 0)
    computer.ram.memory[6] = a.m(ASM.JZ, 0)
    computer.ram.memory[7] = a.m(ASM.JMP, 4)
    computer.ram.memory[15] = 16
