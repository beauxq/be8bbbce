from enum import IntEnum
from collections import defaultdict
from components.signals import Signals
from typing import Dict, Tuple


class ASM(IntEnum):
    """ assembly to machine code """
    NOP = 0
    LDA = 1
    ADD = 2
    SUB = 3
    STA = 4
    LDI = 5
    JMP = 6
    JC = 7
    JZ = 8
    JI = 9  # * my addition - jump indirect
    LIN = 10  # * my addition - load indirect
    SIN = 11  # * my addition - store indirect
    OUT = 14
    HLT = 15


# machine code to assembly
ASM_R: Dict[int, str] = defaultdict(lambda: "NOP", {
    ASM.NOP: "NOP",
    ASM.LDA: "LDA",
    ASM.ADD: "ADD",
    ASM.SUB: "SUB",
    ASM.STA: "STA",
    ASM.LDI: "LDI",
    ASM.JMP: "JMP",
    ASM.JC: "JC ",
    ASM.JZ: "JZ ",
    ASM.JI: "JI ",
    ASM.LIN: "LIN",
    ASM.SIN: "SIN",
    ASM.OUT: "OUT",
    ASM.HLT: "HLT"
})


MICROCODE: Dict[int, Tuple[Tuple[str, ...], Tuple[str, ...], Tuple[str, ...]]] = {
    ASM.NOP: ((), (), ()),
    # no operation

    ASM.LDA: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.REG_A_IN), ()),
    # load value from given memory address into register A

    ASM.ADD: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.REG_B_IN),
              (Signals.ALU_OUT, Signals.REG_A_IN, Signals.FLAGS_IN)),
    # add the value from the given memory address to the value in register A
    # and store the result in register A

    ASM.SUB: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.REG_B_IN),
              (Signals.ALU_OUT, Signals.REG_A_IN,
               Signals.SUBTRACT, Signals.FLAGS_IN)),
    # subtract the value in the given memory address from the value
    # in register A and store the result in register A

    ASM.STA: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.REG_A_OUT, Signals.RAM_IN), ()),
    # store value from register A into given memory address

    ASM.LDI: ((Signals.INSTR_OUT, Signals.REG_A_IN), (), ()),
    # store given value into register A

    ASM.JMP: ((Signals.INSTR_OUT, Signals.COUNTER_IN), (), ()),
    # store given memory address into program counter

    # ASM.JC: Control gives either JMP or NOP
    # store given memory address into program counter if carry flag set

    # ASM.JZ: Control gives either JMP or NOP
    # store given memory address into program counter if zero flag set

    ASM.JI: ((Signals.INSTR_OUT, Signals.MAR_IN),
             (Signals.RAM_OUT, Signals.COUNTER_IN), ()),
    # load value at given memory address into program counter

    ASM.LIN: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.REG_A_IN)),
    # load value from address in given address into register A

    ASM.SIN: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.MAR_IN),
              (Signals.REG_A_OUT, Signals.RAM_IN)),
    # store value from register A into the address in the given memory address

    # undefined nops
    12: ((), (), ()),
    13: ((), (), ()),

    ASM.OUT: ((Signals.REG_A_OUT, Signals.OUTPUT_IN), (), ()),
    # copy the value from register A to output

    ASM.HLT: ((Signals.HALT,), (), ())
    # halt
}


class Assembler:
    def __init__(self, address_length: int):
        self.address_length = address_length

    def m(self, asm: ASM, value: int):
        return (asm << self.address_length) + value


def test():
    print(MICROCODE[ASM.LDA])


if __name__ == "__main__":
    test()
