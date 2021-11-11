from typing import Callable, List
import _pytest.capture
import pytest
from be8bbbce.computer import Computer
from be8bbbce.asm import Assembler

from be8bbbce.programs.programs16bit import addfrsub
# from be8bbbce.programs.programs16bit import bernoulli
from be8bbbce.programs.programs16bit import dividsub
from be8bbbce.programs.programs16bit import gcdsub
from be8bbbce.programs.programs16bit import multfastsub
from be8bbbce.programs.programs16bit import multisub
from be8bbbce.programs.programs16bit import negdivid
from be8bbbce.programs.programs16bit import reducsub


ADDRESS_LENGTH = 12


@pytest.mark.parametrize(("ps", "outputs"), [
    [[addfrsub.p], ["10", "12"]],  # 1/4 + 7/12
    [[multisub.p, dividsub.p], ["42"]],  # 1764 / 42
    [[gcdsub.p], ["42"]],  # gcd(210, 546)
    [[multfastsub.p], ["42"]],  # 7 * 6
    [[multisub.p], ["42"]],  # 8.2537483876 * 5.088597086761041
    [[multisub.p, dividsub.p, negdivid.p], ["-4"]],  # -9 / 2  -2109?
    [[multisub.p, dividsub.p, gcdsub.p, reducsub.p], ["5", "6"]],  # 10/12  2160/3296?
])
def test_programs(capsys: _pytest.capture.CaptureFixture[str],
                  ps: List[Callable[[Computer, Assembler], None]],  # last p is run, depends on earlier ps
                  outputs: List[str]):
    a = Assembler(ADDRESS_LENGTH)
    computer = Computer(ADDRESS_LENGTH)
    computer.control.reset()
    for p in ps:
        p(computer, a)
    print(ps[-1].__doc__)
    computer.clock.go()
    printed = capsys.readouterr()
    for output in outputs:
        # TODO: check that they're in the right order, all in different lines
        assert output in printed.out
