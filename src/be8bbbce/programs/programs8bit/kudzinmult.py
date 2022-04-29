from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler) -> None:
    """  Matthew Kudzin multiply with no conditional jump """
    """
    0:   LDI   0
    1:    STA  15
    2:    LDI    1
    3:    STA   14
    4:    LDA   7
    5:    SUB   14
    6:    STA    7
    7:     <x>
    8:    LDA   15
    9:    ADD   13
    10:  STA   15
    11:   OUT
    12:  JMP   4
    13:  <y>
    """
    computer.ram.memory[0] = a.m(ASM.LDI, 0)
    computer.ram.memory[1] = a.m(ASM.STA, 15)
    computer.ram.memory[2] = a.m(ASM.LDI, 1)
    computer.ram.memory[3] = a.m(ASM.STA, 14)
    computer.ram.memory[4] = a.m(ASM.LDA, 7)
    computer.ram.memory[5] = a.m(ASM.SUB, 14)
    computer.ram.memory[6] = a.m(ASM.STA, 7)
    computer.ram.memory[7] = 7  # x = 7  interpreted as NOP/HLT
    computer.ram.memory[8] = a.m(ASM.LDA, 15)
    computer.ram.memory[9] = a.m(ASM.ADD, 13)
    computer.ram.memory[10] = a.m(ASM.STA, 15)
    computer.ram.memory[11] = a.m(ASM.OUT, 0)
    computer.ram.memory[12] = a.m(ASM.JMP, 4)
    computer.ram.memory[13] = 6  # y = 6
