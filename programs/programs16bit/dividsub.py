from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ divide subroutine at 2200 - requires multiply at 2000 """

    # global utility constants
    computer.ram.memory[4000] = 1 << 15  # min signed
    computer.ram.memory[4001] = 1
    computer.ram.memory[4002] = 0b1111111111111111  # -1 in 16 bits

    divide_subroutine = [
        a.m(ASM.LDI, 1),
        a.m(ASM.STA, 2254),
        a.m(ASM.LDA, 2250),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC , 2206),
        a.m(ASM.JMP, 2211),
        a.m(ASM.LDA, 4002),
        a.m(ASM.STA, 2254),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2250),
        a.m(ASM.STA, 2250),
        a.m(ASM.LDI, 0),
        a.m(ASM.STA, 2255),
        a.m(ASM.LDA, 2250),
        a.m(ASM.SUB, 2251),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC , 2224),
        a.m(ASM.LDA, 2250),
        a.m(ASM.SUB, 2251),
        a.m(ASM.STA, 2250),
        a.m(ASM.LDA, 2255),
        a.m(ASM.ADD, 4001),
        a.m(ASM.STA, 2255),
        a.m(ASM.JMP, 2213),
        a.m(ASM.LDA, 2254),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 2255),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 2231),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),
        a.m(ASM.STA, 2253),
        a.m(ASM.JI , 2252)
    ]
    """
    integer division
    parameters:
    2250 a
    2251 b  must be positive
    2252 pcreturnlocation

    output:
    2253 result

    working variables:
    2254 a_sign
    2255 count
    """

    address = 2200
    for instruction in divide_subroutine:
        computer.ram.memory[address] = instruction
        address += 1

    # use the divide subroutine
    computer.ram.memory[0] = a.m(ASM.LDI, 1764)
    computer.ram.memory[1] = a.m(ASM.STA, 2250)  # a operand
    computer.ram.memory[2] = a.m(ASM.LDI, 42)
    computer.ram.memory[3] = a.m(ASM.STA, 2251)  # b operand
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2252)  # return program counter
    computer.ram.memory[6] = a.m(ASM.JMP, 2200)  # divide subroutine
    computer.ram.memory[7] = a.m(ASM.LDA, 2253)  # result
    computer.ram.memory[8] = a.m(ASM.OUT, 0)
    computer.ram.memory[9] = a.m(ASM.HLT, 0)
