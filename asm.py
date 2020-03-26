from signals import Signals

from enum import IntEnum


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
              (Signals.ALU_OUT, Signals.REG_A_IN, Signals.FLAGS_IN)),
    # add the value from the given memory address to the value in register A
    # and store the result in register A

    ASM.SUB: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.RAM_OUT, Signals.REG_B_IN),
              (Signals.ALU_OUT, Signals.REG_A_IN,
               Signals.SUBTRACT, Signals.FLAGS_IN)),
    # add the value from the given memory address to the value in register A
    # and store the result in register A

    ASM.STA: ((Signals.INSTR_OUT, Signals.MAR_IN),
              (Signals.REG_A_OUT, Signals.RAM_IN), ()),
    # store value from register A into given memory address

    ASM.LDI: ((Signals.INSTR_OUT, Signals.REG_A_IN), (), ()),
    # store value from instruction (4 lsb) into register A

    ASM.JMP: ((Signals.INSTR_OUT, Signals.COUNTER_IN), (), ()),
    # store given memory address into program counter

    # ASM.JC: Control gives either JMP or NOP
    # store given memory address into program counter if carry flag set

    # ASM.JZ: Control gives either JMP or NOP
    # store given memory address into program counter if zero flag set

    ASM.OUT: ((Signals.REG_A_OUT, Signals.OUTPUT_IN), (), ()),
    # copy the value from register A to output

    ASM.HLT: ((Signals.HALT,), (), ())
    # halt
}


def test():
    print(MICROCODE[ASM.LDA])


if __name__ == "__main__":
    test()
