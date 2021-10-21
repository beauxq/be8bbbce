from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ add fractions subroutine at 2100 """

    # global utility constants
    bit_count = computer.bit_count
    computer.ram.memory[4000] = 1 << (bit_count - 1)  # min signed
    computer.ram.memory[4001] = 1
    computer.ram.memory[4002] = (2 ** bit_count) - 1  # -1 in two's complement

    add_fractions_subroutine = [
        a.m(ASM.LDA, 2140),
        a.m(ASM.STA, 2147),
        a.m(ASM.LDA, 2142),
        a.m(ASM.STA, 2145),
        a.m(ASM.LDA, 2141),
        a.m(ASM.STA, 2148),
        a.m(ASM.LDA, 2143),
        a.m(ASM.STA, 2144),
        a.m(ASM.LDA, 2148),  # address 2108
        a.m(ASM.SUB, 2144),
        a.m(ASM.JZ , 2127),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC , 2120),
        a.m(ASM.LDA, 2144),
        a.m(ASM.ADD, 2143),
        a.m(ASM.STA, 2144),
        a.m(ASM.LDA, 2145),
        a.m(ASM.ADD, 2142),
        a.m(ASM.STA, 2145),
        a.m(ASM.JMP, 2108),
        a.m(ASM.LDA, 2148),  # address 2120
        a.m(ASM.ADD, 2141),
        a.m(ASM.STA, 2148),
        a.m(ASM.LDA, 2147),
        a.m(ASM.ADD, 2140),
        a.m(ASM.STA, 2147),
        a.m(ASM.JMP, 2108),
        a.m(ASM.LDA, 2147),  # address 2127
        a.m(ASM.ADD, 2145),
        a.m(ASM.STA, 2147),
        a.m(ASM.JI , 2146)
    ]
    """
    parameters:
    2140  an  operand a numerator
    2141  ad  operand a denominator
    2142  bn  operand b numerator
    2143  bd  operand b denominator
    2146  pc return location

    working variables:
    2144  blcd
    2145  bnm

    result locations:
    2147  anm   result numerator
    2148  alcd  result denominator
    """

    address = 2100
    for instruction in add_fractions_subroutine:
        computer.ram.memory[address] = instruction
        address += 1

    # use the add fractions subroutine
    computer.ram.memory[0] = a.m(ASM.LDI, 1)
    computer.ram.memory[1] = a.m(ASM.STA, 2140)  # a operand numer
    computer.ram.memory[2] = a.m(ASM.LDI, 4)
    computer.ram.memory[3] = a.m(ASM.STA, 2141)  # a operand denom
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2142)  # b operand numer
    computer.ram.memory[6] = a.m(ASM.LDI, 12)
    computer.ram.memory[7] = a.m(ASM.STA, 2143)  # b operand denom
    computer.ram.memory[8] = a.m(ASM.LDI, 11)
    computer.ram.memory[9] = a.m(ASM.STA, 2146)  # return program counter
    computer.ram.memory[10] = a.m(ASM.JMP, 2100)  # add fractions subroutine
    computer.ram.memory[11] = a.m(ASM.LDA, 2147)  # result numer
    computer.ram.memory[12] = a.m(ASM.OUT, 0)
    computer.ram.memory[13] = a.m(ASM.LDA, 2148)  # result denom
    computer.ram.memory[14] = a.m(ASM.OUT, 0)
    computer.ram.memory[15] = a.m(ASM.HLT, 0)
