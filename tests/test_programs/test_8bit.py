from typing import Callable, List
import _pytest.capture
import pytest
from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler

from be8bbbce.programs.programs8bit import p1
from be8bbbce.programs.programs8bit import p2
from be8bbbce.programs.programs8bit import p3
from be8bbbce.programs.programs8bit import p4
from be8bbbce.programs.programs8bit import kudzinmult
from be8bbbce.programs.programs8bit import eatermult
from be8bbbce.programs.programs8bit import fibonacci
from be8bbbce.programs.programs8bit import jumpindirect
from be8bbbce.programs.programs8bit import loadstoreindirect
from be8bbbce.programs.programs8bit import divide
from be8bbbce.programs.programs8bit import sqrt


ADDRESS_LENGTH = 4


@pytest.mark.parametrize(("p", "outputs"), [
    [p1.p, ["42"]],
    [p2.p, ["4"]],
    [p3.p, ["3", "6", "9"]],
    [p4.p, ["0", "16", "32", "48", "176", "160", "144"]],
    [kudzinmult.p, ["42"]],
    [eatermult.p, ["42"]],
    [fibonacci.p, ["0", "1", "1", "2", "3", "5", "8", "13", "21", "34", "55", "144"]],
    [jumpindirect.p, ["3", "6", "9"]],
    [loadstoreindirect.p, ["1", "13", "1"]],
    [divide.p, ["7"]],
    [sqrt.p, ["7"]]
])
def test_programs(capsys: _pytest.capture.CaptureFixture[str],
                  p: Callable[[Computer, Assembler], None],
                  outputs: List[str]):
    a = Assembler(ADDRESS_LENGTH)
    computer = Computer(ADDRESS_LENGTH)
    computer.control.reset()
    p(computer, a)
    print(p.__doc__)
    computer.clock.go(2000)
    printed = capsys.readouterr()
    for output in outputs:
        assert output in printed.out
