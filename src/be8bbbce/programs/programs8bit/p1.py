from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler) -> None:
    """ add 28 + 14 """
    computer.ram.memory[0] = a.m(ASM.LDA, 14)
    computer.ram.memory[1] = a.m(ASM.ADD, 15)
    computer.ram.memory[2] = a.m(ASM.OUT, 0)
    computer.ram.memory[3] = a.m(ASM.HLT, 0)
    computer.ram.memory[14] = 28
    computer.ram.memory[15] = 14
