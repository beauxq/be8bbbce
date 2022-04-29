from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler) -> None:
    """ bounce between signed ints -127 and 127 - remember to flip the 2s complement switch """
    computer.ram.memory[0] = a.m(ASM.LDA, 14)
    computer.ram.memory[1] = a.m(ASM.OUT, 0)
    computer.ram.memory[2] = a.m(ASM.ADD, 15)
    computer.ram.memory[3] = a.m(ASM.STA, 14)
    computer.ram.memory[4] = a.m(ASM.SUB, 13)
    computer.ram.memory[5] = a.m(ASM.JZ, 7)
    computer.ram.memory[6] = a.m(ASM.JMP, 0)
    computer.ram.memory[7] = a.m(ASM.SUB, 15)
    computer.ram.memory[8] = a.m(ASM.STA, 15)
    computer.ram.memory[9] = a.m(ASM.LDA, 14)
    computer.ram.memory[10] = a.m(ASM.ADD, 15)
    computer.ram.memory[11] = a.m(ASM.STA, 14)
    computer.ram.memory[12] = a.m(ASM.JMP, 0)
    computer.ram.memory[13] = 128  # const
    computer.ram.memory[14] = 0  # number counted
    computer.ram.memory[15] = 1  # step size
