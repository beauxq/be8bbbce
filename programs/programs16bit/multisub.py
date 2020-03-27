from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ multiply subroutine at 2000 """

    # global utility constants
    computer.ram.memory[4000] = 1 << 15  # min signed
    computer.ram.memory[4001] = 1
    computer.ram.memory[4002] = 0b1111111111111111  # -1 in 16 bits

    multiply_subroutine = [
        a.m(ASM.LDA, 2033),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC, 2004),
        a.m(ASM.JMP, 2010),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2033),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2034),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 0),
        a.m(ASM.STA, 2036),
        a.m(ASM.LDI, 0),
        a.m(ASM.ADD, 2033),
        a.m(ASM.JZ, 2022),
        a.m(ASM.LDA, 2036),
        a.m(ASM.ADD, 2034),
        a.m(ASM.STA, 2036),
        a.m(ASM.LDA, 2033),
        a.m(ASM.SUB, 4001),
        a.m(ASM.STA, 2033),
        a.m(ASM.JMP, 2012),
        a.m(ASM.JI, 2035)
    ]
    """
    2033 a operand
    2034 b operand
    2035 pc return location
    2036 result location
    """

    address = 2000
    for instruction in multiply_subroutine:
        computer.ram.memory[address] = instruction
        address += 1

    # use the multiply subroutine
    computer.ram.memory[0] = a.m(ASM.LDI, 7)
    computer.ram.memory[1] = a.m(ASM.STA, 2033)  # a operand
    computer.ram.memory[2] = a.m(ASM.LDI, 6)
    computer.ram.memory[3] = a.m(ASM.STA, 2034)  # b operand
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2035)  # return program counter
    computer.ram.memory[6] = a.m(ASM.JMP, 2000)  # multiply subroutine
    computer.ram.memory[7] = a.m(ASM.LDA, 2036)  # result
    computer.ram.memory[8] = a.m(ASM.OUT, 0)
    computer.ram.memory[9] = a.m(ASM.HLT, 0)
