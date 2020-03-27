from computer import Computer
from asm import Assembler, ASM

from programs.programs8bit.p1 import p as p1
from programs.programs8bit.p2 import p as p2
from programs.programs8bit.p3 import p as p3
from programs.programs8bit.p4 import p as p4
from programs.programs8bit.kudzinmult import p as p5
from programs.programs8bit.eatermult import p as p6
from programs.programs8bit.fibonacci import p as p7
from programs.programs8bit.jumpindirect import p as p8


ADDRESS_LENGTH = 4


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
    computer.clock.go(200)

    computer.control.reset()

    p4(computer, a)
    print(p4.__doc__)
    computer.clock.go(400)

    computer.control.reset()

    p5(computer, a)
    print(p5.__doc__)
    computer.clock.go()

    computer.control.reset()

    p6(computer, a)
    print(p6.__doc__)
    computer.clock.go()

    computer.control.reset()

    p7(computer, a)
    print(p7.__doc__)
    computer.clock.go(2000)

    computer.control.reset()

    p8(computer, a)
    print(p8.__doc__)
    computer.clock.go()


if __name__ == "__main__":
    main()
