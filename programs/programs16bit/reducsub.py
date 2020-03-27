from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ reduce fraction subroutine at 2400 - requires divide and gcd """

    # global utility constants
    computer.ram.memory[4000] = 1 << 15  # min signed
    computer.ram.memory[4001] = 1
    computer.ram.memory[4002] = 0b1111111111111111  # -1 in 16 bits

    reduce_subroutine = [
        a.m(ASM.LDA, 2451),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC , 2404),
        a.m(ASM.JMP, 2410),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2450),
        a.m(ASM.STA, 2450),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2451),
        a.m(ASM.STA, 2451),
        a.m(ASM.LDA, 2450),
        a.m(ASM.STA, 2453),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC , 2415),
        a.m(ASM.JMP, 2418),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2453),
        a.m(ASM.STA, 2453),
        a.m(ASM.LDA, 2453),
        a.m(ASM.STA, 2350),
        a.m(ASM.LDA, 2451),
        a.m(ASM.STA, 2351),
        a.m(ASM.LDI, 2425),
        a.m(ASM.STA, 2352),
        a.m(ASM.JMP, 2300),
        a.m(ASM.LDA, 2350),
        a.m(ASM.STA, 2453),
        a.m(ASM.LDA, 2450),
        a.m(ASM.STA, 2250),
        a.m(ASM.LDA, 2453),
        a.m(ASM.STA, 2251),
        a.m(ASM.LDI, 2434),
        a.m(ASM.STA, 2252),
        a.m(ASM.JMP, 2200),
        a.m(ASM.LDA, 2253),
        a.m(ASM.STA, 2450),
        a.m(ASM.LDA, 2451),
        a.m(ASM.STA, 2250),
        a.m(ASM.LDA, 2453),
        a.m(ASM.STA, 2251),
        a.m(ASM.LDI, 2443),
        a.m(ASM.STA, 2252),
        a.m(ASM.JMP, 2200),
        a.m(ASM.LDA, 2253),
        a.m(ASM.STA, 2451),
        a.m(ASM.JI , 2452)
    ]
    """
    parameters:
    2450  n   numerator
    2451  d   denominator
    2452  pc return location

    working variables:
    2453  n_positive and divisor

    result locations:
    2450  n   result numerator
    2451  d   result denominator
    """

    address = 2400
    for instruction in reduce_subroutine:
        computer.ram.memory[address] = instruction
        address += 1

    # use the reduce subroutine
    computer.ram.memory[0] = a.m(ASM.LDI, 10)
    computer.ram.memory[1] = a.m(ASM.STA, 2450)  # n
    computer.ram.memory[2] = a.m(ASM.LDI, 12)
    computer.ram.memory[3] = a.m(ASM.STA, 2451)  # d
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2452)  # return program counter
    computer.ram.memory[6] = a.m(ASM.JMP, 2400)  # gcd subroutine
    computer.ram.memory[7] = a.m(ASM.LDA, 2450)  # result
    computer.ram.memory[8] = a.m(ASM.OUT, 0)
    computer.ram.memory[9] = a.m(ASM.LDA, 2451)  # result
    computer.ram.memory[10] = a.m(ASM.OUT, 0)
    computer.ram.memory[11] = a.m(ASM.HLT, 0)
