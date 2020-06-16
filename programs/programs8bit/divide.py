from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ integer division:  42 / 6 """
    computer.ram.memory[0] = a.m(ASM.LDA, 14)
    computer.ram.memory[1] = a.m(ASM.SUB, 15)
    computer.ram.memory[2] = a.m(ASM.JC, 6)  # if subtraction didn't go below 0
    computer.ram.memory[3] = a.m(ASM.LDA, 13)
    computer.ram.memory[4] = a.m(ASM.OUT, 0)
    computer.ram.memory[5] = a.m(ASM.HLT, 0)
    computer.ram.memory[6] = a.m(ASM.STA, 14)
    computer.ram.memory[7] = a.m(ASM.LDA, 13)
    computer.ram.memory[8] = a.m(ASM.ADD, 12)
    computer.ram.memory[9] = a.m(ASM.STA, 13)
    computer.ram.memory[10] = a.m(ASM.JMP, 0)
    computer.ram.memory[11] = a.m(ASM.NOP, 0)
    computer.ram.memory[12] = 1  # const
    computer.ram.memory[13] = 0  # count subtractions
    computer.ram.memory[14] = 42  # x = 42
    computer.ram.memory[15] = 6  # y = 6
