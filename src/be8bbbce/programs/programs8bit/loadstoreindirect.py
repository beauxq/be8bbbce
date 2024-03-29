from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler) -> None:
    """ load and store indirect (1 13 1) """
    computer.ram.memory[0] = a.m(ASM.LIN, 13)
    computer.ram.memory[1] = a.m(ASM.OUT, 0)  # 1
    computer.ram.memory[2] = a.m(ASM.LDA, 13)
    computer.ram.memory[3] = a.m(ASM.ADD, 14)
    computer.ram.memory[4] = a.m(ASM.SIN, 15)
    computer.ram.memory[5] = a.m(ASM.LIN, 13)
    computer.ram.memory[6] = a.m(ASM.OUT, 0)  # 13
    computer.ram.memory[7] = a.m(ASM.LDA, 13)
    computer.ram.memory[8] = a.m(ASM.SUB, 14)
    computer.ram.memory[9] = a.m(ASM.STA, 13)
    computer.ram.memory[10] = a.m(ASM.LIN, 13)
    computer.ram.memory[11] = a.m(ASM.OUT, 0)  # 1
    computer.ram.memory[12] = a.m(ASM.HLT, 0)
    computer.ram.memory[13] = 14
    computer.ram.memory[14] = 1
    computer.ram.memory[15] = 13
