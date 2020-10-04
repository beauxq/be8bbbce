from computer import Computer
from asm import Assembler, ASM


def p(computer: Computer, a: Assembler):
    """ Ada Lovelace's Bernoulli number calculator """

    bernoulli = [
        a.m(ASM.LDI, 1),
        a.m(ASM.STA, 1010),
        a.m(ASM.LDI, 2),
        a.m(ASM.STA, 1020),
        a.m(ASM.LDI, 0),
        a.m(ASM.STA, 1070),
        a.m(ASM.STA, 1130),
        # op1 v4,v5,v6 = v2 * v3
        a.m(ASM.LDA, 1020),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 1030),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 14),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 14
        a.m(ASM.STA, 1040),
        a.m(ASM.STA, 1050),
        a.m(ASM.STA, 1060),
        # op2 v4 = v4 - v1
        a.m(ASM.LDA, 1040),
        a.m(ASM.SUB, 1010),
        a.m(ASM.STA, 1040),
        # op3 v5 = v5 + v1
        a.m(ASM.LDA, 1050),
        a.m(ASM.ADD, 1010),
        a.m(ASM.STA, 1050),
        # op4 v11f = v4 / v5
        a.m(ASM.STA, 1111),
        a.m(ASM.LDA, 1040),
        a.m(ASM.STA, 1110),
        # op5 v11 = v11 / v2 -> v11d = multiply(v11d, v2i)
        a.m(ASM.LDA, 1111),
        a.m(ASM.STA, 2034),  # better when a is lower number
        a.m(ASM.LDA, 1020),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDI, 34),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 34
        a.m(ASM.STA, 1111),
        # op6 v13 = v13 - v11
        # v13n = v13n - v11n; v13d = v11d
        # v13n, v13d = reduce(v13n, v13d)
        # TODO: remove this reduce, there's no way this isn't already reduced
        a.m(ASM.LDA, 1130),
        a.m(ASM.SUB, 1110),
        a.m(ASM.STA, 2450),  # store in reduce parameter
        a.m(ASM.LDA, 1111),
        a.m(ASM.STA, 2451),
        a.m(ASM.LDI, 44),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2450),  # address 44
        a.m(ASM.STA, 1130),
        a.m(ASM.LDA, 2451),
        a.m(ASM.STA, 1131),
        # op7 v10i = v3i - v1i
        a.m(ASM.LDA, 1030),
        a.m(ASM.SUB, 1010),
        a.m(ASM.STA, 1100),  # on first run, v10 is now 1
        # op8 v7i = v2i + v7i
        a.m(ASM.LDA, 1020),
        a.m(ASM.ADD, 1070),
        a.m(ASM.STA, 1070),
        # op9 v11 = v6 / v7 ~ v11n = v6i; v11d = v7i
        a.m(ASM.STA, 1111),
        a.m(ASM.LDA, 1060),
        a.m(ASM.STA, 1110),
        # op10 v12 = v20[1] * v11
        # v12n = multiply(v20n[1], v11n)
        # v12d = multiply(v20d[1], v11d)
        a.m(ASM.LDA, 1210),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 1110),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 64),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 64
        a.m(ASM.STA, 1120),
        a.m(ASM.LDA, 1211),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 1111),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 73),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 73
        a.m(ASM.STA, 1121),
        # op11 v13 = v12 + v13
        # v13n, v13d = add_f(v12n, v12d, v13n, v13d)
        # v13n, v13d = red(v13n, v13d)
        a.m(ASM.LDA, 1120),
        a.m(ASM.STA, 2140),
        a.m(ASM.LDA, 1121),
        a.m(ASM.STA, 2141),
        a.m(ASM.LDA, 1130),
        a.m(ASM.STA, 2142),
        a.m(ASM.LDA, 1131),
        a.m(ASM.STA, 2143),
        a.m(ASM.LDI, 86),
        a.m(ASM.STA, 2146),
        a.m(ASM.JMP, 2100),
        a.m(ASM.LDA, 2147),  # address 86 - from output of add
        a.m(ASM.STA, 2450),  # to input of reduce
        a.m(ASM.LDA, 2148),
        a.m(ASM.STA, 2451),
        a.m(ASM.LDI, 93),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2450),  # address 93
        a.m(ASM.STA, 1130),
        a.m(ASM.LDA, 2451),
        a.m(ASM.STA, 1131),
        # op12 v10i = v10i - v1i
        a.m(ASM.LDA, 1100),
        a.m(ASM.SUB, 1010),
        a.m(ASM.STA, 1100),  # first run v10 is now 0
        # while v10i > 0
        # both here and before I jump back here,
        # v10 in reg A, zero flag set if 0
        a.m(ASM.JZ, 245),  # address 100
        # op13 v6i = v6i - v1i
        a.m(ASM.LDA, 1060),
        a.m(ASM.SUB, 1010),
        a.m(ASM.STA, 1060),
        # op14 v7i = v1i + v7i
        a.m(ASM.LDA, 1010),
        a.m(ASM.ADD, 1070),
        a.m(ASM.STA, 1070),
        # op15 v8 = v6 / v7
        # v8n = v6i
        # v8d = v7i
        # v8n, v8d = reduce(v8n, v8d)
        a.m(ASM.STA, 2451),  # v7 already in mem, to reduce param
        a.m(ASM.LDA, 1060),
        a.m(ASM.STA, 2450),
        a.m(ASM.LDI, 113),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2451),  # address 113
        a.m(ASM.STA, 1081),
        a.m(ASM.LDA, 2450),
        a.m(ASM.STA, 1080),
        # op16 v11 = v8 * v11  ~  mult n; mult d; then reduce
        a.m(ASM.STA, 2033),  # v8n already in reg A
        a.m(ASM.LDA, 1110),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 123),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 123 - numer to be reduced
        a.m(ASM.STA, 2450),  # leave that there for a bit
        a.m(ASM.LDA, 1081),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 1111),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 132),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 132 - denom
        a.m(ASM.STA, 2451),  # to be reduced
        a.m(ASM.LDI, 137),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2450),  # address 137
        a.m(ASM.STA, 1110),
        a.m(ASM.LDA, 2451),
        a.m(ASM.STA, 1111),
        # op17 v6i = v6i - v1i
        a.m(ASM.LDA, 1060),
        a.m(ASM.SUB, 1010),
        a.m(ASM.STA, 1060),
        # op18 v7i = v1i + v7i
        a.m(ASM.LDA, 1010),
        a.m(ASM.ADD, 1070),
        a.m(ASM.STA, 1070),
        # op19 v9 = v6i / v7i  ~  reduce then put in v9
        a.m(ASM.STA, 2451),  # v7 already in reg A
        a.m(ASM.LDA, 1060),
        a.m(ASM.STA, 2450),
        a.m(ASM.LDI, 153),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2451),  # address 153 - denom first
        a.m(ASM.STA, 1091),
        a.m(ASM.LDA, 2450),
        a.m(ASM.STA, 1090),
        # op20 v11 = v9 * v11
        # mult n; mult d; then reduce ~ copy paste from op16
        a.m(ASM.STA, 2033),  # v9n already in reg A
        a.m(ASM.LDA, 1110),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 163),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 163 - numer to be reduced
        a.m(ASM.STA, 2450),  # leave that there for a bit
        a.m(ASM.LDA, 1091),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 1111),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 172),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 172 - denom
        a.m(ASM.STA, 2451),  # to be reduced
        a.m(ASM.LDI, 177),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2450),  # address 177
        a.m(ASM.STA, 1110),
        a.m(ASM.LDA, 2451),
        a.m(ASM.STA, 1111),
        # op21 v12 = v20[v3i - v10i] * v11
        # mult(v20n[v3i - v10i], v11n); then d; then reduce
        a.m(ASM.NOP, 0),  # for safety - wiggle room for fixing mistakes
        # about to make address for v20n[v3i - v10i]
        a.m(ASM.LDA, 1030),  # v3i
        a.m(ASM.SUB, 1100),  # - v10i
        a.m(ASM.STA, 2033),
        a.m(ASM.LDI, 10),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 190),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDI, 1200),  # address 190
        a.m(ASM.ADD, 2036),  # 1200 + (v3i - v10i) * 10
        a.m(ASM.STA, 900),  # address of v20n[v3i - v10i]
        a.m(ASM.ADD, 1010),
        a.m(ASM.STA, 901),  # address of v20d[v3i - v10i]
        a.m(ASM.LIN, 900),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 1110),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 202),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 202 - numer to be reduced
        a.m(ASM.STA, 2450),  # leave that there for a bit
        a.m(ASM.LIN, 901),
        a.m(ASM.STA, 2033),
        a.m(ASM.LDA, 1111),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 211),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDA, 2036),  # address 211 - denom to be reduced
        a.m(ASM.STA, 2451),
        a.m(ASM.LDI, 216),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2451),  # address 216 - d first to have n in register
        a.m(ASM.STA, 1121),
        a.m(ASM.LDA, 2450),
        a.m(ASM.STA, 1120),
        # op22 v13 = v12 + v13  ~  add fractions and reduce
        a.m(ASM.STA, 2140),  # v12n already in register
        a.m(ASM.LDA, 1121),
        a.m(ASM.STA, 2141),
        a.m(ASM.LDA, 1130),
        a.m(ASM.STA, 2142),
        a.m(ASM.LDA, 1131),
        a.m(ASM.STA, 2143),
        a.m(ASM.LDI, 230),
        a.m(ASM.STA, 2146),
        a.m(ASM.JMP, 2100),
        a.m(ASM.LDA, 2147),  # address 230
        a.m(ASM.STA, 2450),
        a.m(ASM.LDA, 2148),
        a.m(ASM.STA, 2451),
        a.m(ASM.LDI, 237),
        a.m(ASM.STA, 2452),
        a.m(ASM.JMP, 2400),
        a.m(ASM.LDA, 2450),  # address 237
        a.m(ASM.STA, 1130),
        a.m(ASM.LDA, 2451),
        a.m(ASM.STA, 1131),
        # op23 v10i = v10i - v1i
        a.m(ASM.LDA, 1100),
        a.m(ASM.SUB, 1010),  # this will set zero flag if v10 == 0
        a.m(ASM.STA, 1100),
        a.m(ASM.JMP, 100),
        # op24 v20[v3i] = v20[v3i] - v13
        # v20n[v3i] = v20n[v3i] - v13n; v20d[v3i] = v13d
        a.m(ASM.LDA, 1030),  # address 245
        a.m(ASM.STA, 2033),
        a.m(ASM.LDI, 10),
        a.m(ASM.STA, 2034),
        a.m(ASM.LDI, 252),
        a.m(ASM.STA, 2035),
        a.m(ASM.JMP, 2000),
        a.m(ASM.LDI, 1200),  # address 252
        a.m(ASM.ADD, 2036),
        a.m(ASM.STA, 900),  # v20n[v3i]
        a.m(ASM.ADD, 1010),
        a.m(ASM.STA, 901),  # v20d[v3i]
        a.m(ASM.LIN, 900),
        a.m(ASM.SUB, 1130),
        a.m(ASM.OUT, 0),  # numerator of bern
        a.m(ASM.SIN, 900),
        a.m(ASM.LDA, 1131),
        a.m(ASM.SIN, 901),
        a.m(ASM.OUT, 0),  # denominator of bern
        # op25 v3i = v1i + v3i
        a.m(ASM.LDA, 1010),
        a.m(ASM.ADD, 1030),
        a.m(ASM.STA, 1030),
        a.m(ASM.HLT, 0)  # [267] or JMP, 0    (or JMP, 4 don't need 0-3)
    ]

    address = 0
    for instruction in bernoulli:
        computer.ram.memory[address] = instruction
        address += 1

    # data initializations:
    computer.ram.memory[1030] = 2
    # will increment with each run of the program
    # this is which bernoulli number is being calculated
    computer.ram.memory[1210] = 1  # the numerator of the first bern number
    computer.ram.memory[1211] = 6  # the denominator of the first bern number

    # all of the v20n need to be initialized to 0
    # (1220, 1230, 1240, ...) as far as we want to go
    for i in range(1220, 2000, 10):
        computer.ram.memory[i] = 0
