from be8bbbce.computer import Computer, INSTRUCTION_LENGTH
from be8bbbce.asm import Assembler, ASM

from be8bbbce.programs.programs16bit.multisub import p as p1
from be8bbbce.programs.programs16bit.dividsub import p as p2
from be8bbbce.programs.programs16bit.gcdsub import p as p4
from be8bbbce.programs.programs16bit.addfrsub import p as p5
from be8bbbce.programs.programs16bit.reducsub import p as p6

from be8bbbce.programs.programs16bit.bernoulli import p as bern


ADDRESS_LENGTH = 28
BIT_COUNT = INSTRUCTION_LENGTH + ADDRESS_LENGTH  # 4 + 28 = 32


def main() -> None:
    a = Assembler(ADDRESS_LENGTH)

    print("initializing computer...")
    computer = Computer(ADDRESS_LENGTH, True)

    print("programming computer...")
    p1(computer, a)
    p2(computer, a)
    p4(computer, a)
    p5(computer, a)
    p6(computer, a)
    bern(computer, a)

    computer.ram.memory[267] = a.m(ASM.JMP, 4)
    # reset instead of halt to compute next

    print("running")
    computer.clock.go()


if __name__ == "__main__":
    main()
