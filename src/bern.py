from be8bbbce.computer import Computer, INSTRUCTION_LENGTH
from be8bbbce.asm import Assembler

from be8bbbce.programs.programs16bit.multisub import p as p1
from be8bbbce.programs.programs16bit.dividsub import p as p2
from be8bbbce.programs.programs16bit.negdivid import p as p3
from be8bbbce.programs.programs16bit.gcdsub import p as p4
from be8bbbce.programs.programs16bit.addfrsub import p as p5
from be8bbbce.programs.programs16bit.reducsub import p as p6

from be8bbbce.programs.programs16bit.bernoulli import p as bern


ADDRESS_LENGTH = 12
BIT_COUNT = INSTRUCTION_LENGTH + ADDRESS_LENGTH  # 4 + 12 = 16


def main():
    a = Assembler(ADDRESS_LENGTH)

    computer = Computer(ADDRESS_LENGTH)

    p1(computer, a)
    print(p1.__doc__)
    computer.clock.go()

    computer.control.reset()

    p2(computer, a)
    print(p2.__doc__)
    computer.clock.go()

    computer.control.reset()

    p3(computer, a)
    print(p3.__doc__)
    computer.clock.go()

    computer.control.reset()

    p4(computer, a)
    print(p4.__doc__)
    computer.clock.go()

    computer.control.reset()

    p5(computer, a)
    print(p5.__doc__)
    computer.clock.go()

    computer.control.reset()

    p6(computer, a)
    print(p6.__doc__)
    computer.clock.go()

    computer.control.reset()

    bern(computer, a)
    print(bern.__doc__)
    computer.clock.go()


if __name__ == "__main__":
    main()
