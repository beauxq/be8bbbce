from be8bbbce.computer import Computer
from be8bbbce.visualcomponents.visualmain import VisualMain


def test(patch_pygame: None):

    c = Computer(4)
    vm = VisualMain(c)

    assert vm.paused
    assert vm.fps > 22

    # vm.run()
