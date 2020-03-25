from signals import Signals

from enum import IntEnum


class ASM(IntEnum):
    """ assembly to machine code """
    NOP = 0
    LDA = 1
    ADD = 2
    OUT = 14
    HLT = 15


MICROCODE = {
    ASM.NOP: ((), (), ()),
    # no operation

    ASM.LDA: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.REG_A_IN), ()),
    # load value from given memory address into register A

    ASM.ADD: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.REG_B_IN),
              (Signals.ALU_OUT, Signals.REG_A_IN)),
    # add the value from the given memory address to the value in register A
    # and store the result in register A

    ASM.OUT: ((Signals.REG_A_OUT, Signals.OUTPUT_IN), (), ()),
    # copy the value from register A to output

    ASM.HLT: ((Signals.HALT,), (), ())
    # halt
}


def test():
    print(MICROCODE[ASM.LDA])


if __name__ == "__main__":
    test()
