from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler

from be8bbbce.programs.programs8bit.p1 import p as p1
from be8bbbce.programs.programs8bit.p2 import p as p2
from be8bbbce.programs.programs8bit.p3 import p as p3
from be8bbbce.programs.programs8bit.p4 import p as p4
from be8bbbce.programs.programs8bit.kudzinmult import p as p5
from be8bbbce.programs.programs8bit.eatermult import p as p6
from be8bbbce.programs.programs8bit.fibonacci import p as p7
from be8bbbce.programs.programs8bit.jumpindirect import p as p8
from be8bbbce.programs.programs8bit.loadstoreindirect import p as p9
from be8bbbce.programs.programs8bit.divide import p as p10
from be8bbbce.programs.programs8bit.sqrt import p as p11

PS = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]


ADDRESS_LENGTH = 4


def main():
    a = Assembler(ADDRESS_LENGTH)

    computer = Computer(ADDRESS_LENGTH)

    for p in PS:
        computer.control.reset()
        p(computer, a)
        print(p.__doc__)
        computer.clock.go(2000)


if __name__ == "__main__":
    main()
