from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ use divide subroutine to test negative division """

    computer.ram.memory[0] = a.m(ASM.LDA, 15)
    computer.ram.memory[1] = a.m(ASM.STA, 2250)  # a operand
    computer.ram.memory[2] = a.m(ASM.LDI, 2)
    computer.ram.memory[3] = a.m(ASM.STA, 2251)  # b operand
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2252)  # return program counter
    computer.ram.memory[6] = a.m(ASM.JMP, 2200)  # divide subroutine
    computer.ram.memory[7] = a.m(ASM.LDA, 2253)  # result
    computer.ram.memory[8] = a.m(ASM.OUT, 0)
    computer.ram.memory[9] = a.m(ASM.HLT, 0)

    computer.ram.memory[15] = 0b1111111111110111  # -9
