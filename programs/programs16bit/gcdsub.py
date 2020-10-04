from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ gcd subroutine at 2300 """

    # global utility constants
    bit_count = computer.bit_count
    computer.ram.memory[4000] = 1 << (bit_count - 1)  # min signed
    computer.ram.memory[4001] = 1
    computer.ram.memory[4002] = (2 ** bit_count) - 1  # -1 in two's complement

    gcd_subroutine = [
        a.m(ASM.LDA, 2350),
        a.m(ASM.SUB, 2351),
        a.m(ASM.JZ , 2313),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC , 2309),
        a.m(ASM.LDA, 2350),
        a.m(ASM.SUB, 2351),
        a.m(ASM.STA, 2350),
        a.m(ASM.JMP, 2300),
        a.m(ASM.LDA, 2351),  # address 2309
        a.m(ASM.SUB, 2350),
        a.m(ASM.STA, 2351),
        a.m(ASM.JMP, 2300),
        a.m(ASM.JI , 2352)  # address 2313
    ]
    """
    parameters:
    2350 a  must be positive
    2351 b  must be positive
    2352 pc return location

    output:
    2350 result
    """

    address = 2300
    for instruction in gcd_subroutine:
        computer.ram.memory[address] = instruction
        address += 1

    # use the gcd subroutine
    computer.ram.memory[0] = a.m(ASM.LDI, 210)
    computer.ram.memory[1] = a.m(ASM.STA, 2350)  # a operand
    computer.ram.memory[2] = a.m(ASM.LDI, 546)
    computer.ram.memory[3] = a.m(ASM.STA, 2351)  # b operand
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2352)  # return program counter
    computer.ram.memory[6] = a.m(ASM.JMP, 2300)  # gcd subroutine
    computer.ram.memory[7] = a.m(ASM.LDA, 2350)  # result
    computer.ram.memory[8] = a.m(ASM.OUT, 0)
    computer.ram.memory[9] = a.m(ASM.HLT, 0)
