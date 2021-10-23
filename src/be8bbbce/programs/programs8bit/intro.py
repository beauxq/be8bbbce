from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """
    show powers of 2 and 0
    seen in the introduction video linked in the readme

    (not exactly the same program as in the video --
    he modified the instruction set between the 2 computers
    and he put the main loop of this first, and the reset after)
    """
    computer.ram.memory[0] = a.m(ASM.LDI, 0)
    computer.ram.memory[1] = a.m(ASM.NOP, 0)
    computer.ram.memory[2] = a.m(ASM.OUT, 0)
    computer.ram.memory[3] = a.m(ASM.NOP, 0)
    computer.ram.memory[4] = a.m(ASM.NOP, 0)
    computer.ram.memory[5] = a.m(ASM.LDI, 1)
    computer.ram.memory[6] = a.m(ASM.STA, 15)
    computer.ram.memory[7] = a.m(ASM.OUT, 0)
    computer.ram.memory[8] = a.m(ASM.ADD, 15)
    computer.ram.memory[9] = a.m(ASM.JC, 0)
    computer.ram.memory[10] = a.m(ASM.JMP, 6)
