from computer import Computer, INSTRUCTION_LENGTH
from asm import Assembler, ASM

ADDRESS_LENGTH = 12
BIT_COUNT = INSTRUCTION_LENGTH + ADDRESS_LENGTH


def main():
    a = Assembler(ADDRESS_LENGTH)

    computer = Computer(ADDRESS_LENGTH)

    # global utility constants
    computer.ram.memory[4000] = 1 << (BIT_COUNT - 1)  # min signed
    computer.ram.memory[4001] = 1

    print(" multiply subroutine")
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

    computer.clock.go()

    computer.control.reset()

    print(" divide subroutine")
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

    computer.clock.go()

    computer.control.reset()

    print(" gcd subroutine")
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
        a.m(ASM.LDA, 2351),
        a.m(ASM.SUB, 2350),
        a.m(ASM.STA, 2351),
        a.m(ASM.JMP, 2300),
        a.m(ASM.JI , 2352)
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

    computer.clock.go()

    computer.control.reset()

    print(" add fractions subroutine")
    add_fractions_subroutine = [
        a.m(ASM.LDA, 2140),
        a.m(ASM.STA, 2147),
        a.m(ASM.LDA, 2142),
        a.m(ASM.STA, 2145),
        a.m(ASM.LDA, 2141),
        a.m(ASM.STA, 2148),
        a.m(ASM.LDA, 2143),
        a.m(ASM.STA, 2144),
        a.m(ASM.LDA, 2148),
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
        a.m(ASM.LDA, 2148),
        a.m(ASM.ADD, 2141),
        a.m(ASM.STA, 2148),
        a.m(ASM.LDA, 2147),
        a.m(ASM.ADD, 2140),
        a.m(ASM.STA, 2147),
        a.m(ASM.JMP, 2108),
        a.m(ASM.LDA, 2147),
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

    computer.clock.go()


if __name__ == "__main__":
    main()
