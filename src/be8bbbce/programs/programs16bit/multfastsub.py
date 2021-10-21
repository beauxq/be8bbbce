from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ multiply subroutine at 2000
    faster for big numbers
    slower for small numbers """

    # global utility constants
    bit_count = computer.bit_count
    computer.ram.memory[4000] = 1 << (bit_count - 1)  # min signed
    computer.ram.memory[4001] = 1
    computer.ram.memory[4002] = (2 ** bit_count) - 1  # -1 in two's complement

    multiply_subroutine = [
        a.m(ASM.LDA, 2080),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC,  2004),
        a.m(ASM.JMP, 2010),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2080),
        a.m(ASM.STA, 2080),
        a.m(ASM.LDI, 0),
        a.m(ASM.SUB, 2081),
        a.m(ASM.STA, 2081),
        a.m(ASM.LDI, 0),
        a.m(ASM.STA, 2083),
        a.m(ASM.LDI, 0),
        a.m(ASM.ADD, 2080),
        a.m(ASM.JZ,  2076),
        a.m(ASM.LDI, 1),
        a.m(ASM.STA, 2086),
        a.m(ASM.STA, 2088),
        a.m(ASM.LDA, 2081),
        a.m(ASM.STA, 2083),
        a.m(ASM.SIN, 2084),
        a.m(ASM.LDI, 2),
        a.m(ASM.STA, 2089),
        a.m(ASM.LDA, 2080),
        a.m(ASM.SUB, 2089),
        a.m(ASM.JC,  2027),
        a.m(ASM.JMP, 2045),
        a.m(ASM.LDA, 2083),
        a.m(ASM.ADD, 2083),
        a.m(ASM.STA, 2083),
        a.m(ASM.LDA, 2088),
        a.m(ASM.ADD, 2088),
        a.m(ASM.STA, 2088),
        a.m(ASM.LDA, 2086),
        a.m(ASM.ADD, 2084),
        a.m(ASM.STA, 2087),
        a.m(ASM.LDA, 2083),
        a.m(ASM.SIN, 2087),
        a.m(ASM.LDA, 2088),
        a.m(ASM.ADD, 2088),
        a.m(ASM.STA, 2089),
        a.m(ASM.LDI, 1),
        a.m(ASM.ADD, 2086),
        a.m(ASM.STA, 2086),
        a.m(ASM.JMP, 2023),
        a.m(ASM.LDA, 2086),
        a.m(ASM.SUB, 2090),
        a.m(ASM.STA, 2086),
        a.m(ASM.ADD, 4000),
        a.m(ASM.JC, 2076),
        a.m(ASM.LDA, 2086),
        a.m(ASM.ADD, 2085),
        a.m(ASM.STA, 2087),
        a.m(ASM.LIN, 2087),
        a.m(ASM.ADD, 2088),
        a.m(ASM.STA, 2087),
        a.m(ASM.LDA, 2080),
        a.m(ASM.SUB, 2087),
        a.m(ASM.JC, 2060),
        a.m(ASM.JMP, 2072),
        a.m(ASM.LDA, 2086),
        a.m(ASM.ADD, 2084),
        a.m(ASM.STA, 2087),
        a.m(ASM.LIN, 2087),
        a.m(ASM.ADD, 2083),
        a.m(ASM.STA, 2083),
        a.m(ASM.LDA, 2086),
        a.m(ASM.ADD, 2085),
        a.m(ASM.STA, 2087),
        a.m(ASM.LIN, 2087),
        a.m(ASM.ADD, 2088),
        a.m(ASM.STA, 2088),
        a.m(ASM.LDA, 2086),
        a.m(ASM.SUB, 4001),
        a.m(ASM.STA, 2086),
        a.m(ASM.JMP, 2048),
        a.m(ASM.JI, 2082)
    ]
    """
    2080 a operand
    2081 b operand
    2082 pc return location
    2083 result

    2084 powers (pointer)
    2085 addition counts (pointer)
    2086 cache index
    2087 pointer (temp)
    2088 additions done
    2089 double
    2090 2 const

    400 powers 
    500-564 addition counts
    """

    # place those constants ^
    computer.ram.memory[2084] = 400
    computer.ram.memory[2085] = 500
    computer.ram.memory[2090] = 2

    for i in range(500, 565):
        computer.ram.memory[i] = 2 ** (i - 500)

    address = 2000
    for instruction in multiply_subroutine:
        computer.ram.memory[address] = instruction
        address += 1

    # use the multiply subroutine
    computer.ram.memory[0] = a.m(ASM.LDI, 7)
    computer.ram.memory[1] = a.m(ASM.STA, 2080)  # a operand
    computer.ram.memory[2] = a.m(ASM.LDI, 6)
    computer.ram.memory[3] = a.m(ASM.STA, 2081)  # b operand
    computer.ram.memory[4] = a.m(ASM.LDI, 7)
    computer.ram.memory[5] = a.m(ASM.STA, 2082)  # return program counter
    computer.ram.memory[6] = a.m(ASM.JMP, 2000)  # multiply subroutine
    computer.ram.memory[7] = a.m(ASM.LDA, 2083)  # result
    computer.ram.memory[8] = a.m(ASM.OUT, 0)
    computer.ram.memory[9] = a.m(ASM.HLT, 0)
