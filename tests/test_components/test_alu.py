from typing import Callable, Tuple
from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus
from be8bbbce.components.register import RegisterInOut
from be8bbbce.components.alu import ALU
import pytest


@pytest.fixture
def alu():
    signals = Signals()
    bus = Bus()
    reg_a = RegisterInOut(signals, bus, Signals.REG_A_IN, Signals.REG_A_OUT)
    reg_b = RegisterInOut(signals, bus, Signals.REG_B_IN, Signals.REG_B_OUT)
    # TODO: test other word lengths
    return ALU(signals, bus, reg_a, reg_b, 8)


AASType = Tuple[ALU, Callable[[int, int, int, int], None], Callable[[int, int, int, int], None]]


@pytest.fixture
def alu_add_subtract(alu: ALU) -> AASType:
    def arithmetic(a: int, b: int, result: int, carry: int, subtract: int):
        # set subtract input directly
        alu.reg_a.value = a
        alu.reg_b.value = b
        alu.subtract = subtract
        alu.signals.signal(Signals.CLOCK, 1)
        alu.signals.signal(Signals.CLOCK, 0)
        assert alu.value == result
        assert alu.carry == carry

        # send subtract signal
        alu.reg_a.value = a
        alu.reg_b.value = b
        alu.signals.signal(Signals.SUBTRACT, subtract)
        alu.signals.signal(Signals.CLOCK, 1)
        alu.signals.signal(Signals.CLOCK, 0)
        assert alu.value == result
        assert alu.carry == carry

    def add(a: int, b: int, result: int, carry: int):
        arithmetic(a, b, result, carry, 0)

    def subtract(a: int, b: int, result: int, carry: int):
        arithmetic(a, b, result, carry, 1)

    return alu, add, subtract


def test_twos_complement(alu: ALU) -> None:
    assert alu.twos_complement_negation(0) == 0
    assert alu.twos_complement_negation(1) == 255
    assert alu.twos_complement_negation(255) == 1
    assert alu.twos_complement_negation(2) == 254
    assert alu.twos_complement_negation(254) == 2
    for i in range(3, 254):
        assert alu.twos_complement_negation(i) == 256 - i

    assert alu.twos_complement_negation(0b00101100) == 0b11010100
    assert alu.twos_complement_negation(0b10011111) == 0b01100001
    assert alu.twos_complement_negation(0b00100101) == 0b11011011
    assert alu.twos_complement_negation(0b10011000) == 0b01101000


def test_arithmetic(alu_add_subtract: AASType) -> None:
    alu, add, subtract = alu_add_subtract
    add(6, 2, 8, 0)

    add(125, 5, 130, 0)
    add(125, 5, alu.twos_complement_negation(126), 0)

    add(250, 10, 4, 1)
    add(alu.twos_complement_negation(6), 10, 4, 1)

    subtract(10, 20, 246, 0)
    subtract(10, 20, alu.twos_complement_negation(10), 0)

    add(246, 20, 10, 1)
    add(alu.twos_complement_negation(10), 20, 10, 1)

    add(10, 236, 246, 0)
    add(10, alu.twos_complement_negation(20), alu.twos_complement_negation(10), 0)

    add(246, 236, 226, 1)
    add(alu.twos_complement_negation(10),
        alu.twos_complement_negation(20),
        alu.twos_complement_negation(30),
        1)

    subtract(246, 236, 10, 1)
    subtract(alu.twos_complement_negation(10),
             alu.twos_complement_negation(20),
             10,
             1)

    # below are the test cases Ben Eater spent time with in his videos

    add(0, 8, 8, 0)

    subtract(0, 8, 8 + 16 + 32 + 64 + 128, 0)
    subtract(0, 8, alu.twos_complement_negation(8), 0)

    add(64, 0, 64, 0)

    add(0, 4, 4, 0)

    subtract(6, 2, 4, 1)

    def alu_to_a() -> None:
        """
        move value from alu to reg a to keep counting down by the value in b
        """
        alu.signals.signal(Signals.ALU_OUT, 1)
        alu.signals.signal(Signals.REG_A_IN, 1)
        alu.signals.signal(Signals.CLOCK, 1)
        alu.signals.signal(Signals.CLOCK, 0)
        alu.signals.signal(Signals.ALU_OUT, 0)
        alu.signals.signal(Signals.REG_A_IN, 0)

    alu_to_a()
    assert alu.value == 2
    assert alu.carry == 1

    alu_to_a()
    assert alu.value == 0
    assert alu.carry == 1

    alu_to_a()
    assert alu.value == 254
    assert alu.carry == 0

    alu_to_a()
    assert alu.value == 252
    assert alu.carry == 1


def test_subtract_carry(alu_add_subtract: AASType) -> None:
    """
    carry is confusing with subtraction
    """
    alu, _, subtract = alu_add_subtract

    neg127 = alu.twos_complement_negation(127)
    neg128 = alu.twos_complement_negation(128)

    # subtracting a positive number
    # carries unless going from non-negative to negative
    subtract(5, 2, 3, 1)
    subtract(2, 2, 0, 1)
    subtract(1, 2, alu.twos_complement_negation(1), 0)
    subtract(0, 2, alu.twos_complement_negation(2), 0)
    subtract(alu.twos_complement_negation(1), 2, alu.twos_complement_negation(3), 1)
    subtract(alu.twos_complement_negation(2), 2, alu.twos_complement_negation(4), 1)
    subtract(alu.twos_complement_negation(3), 2, alu.twos_complement_negation(5), 1)

    subtract(neg128, 2, 126, 1)
    subtract(neg127, 2, 127, 1)
    subtract(127, 2, 125, 1)

    subtract(neg128, 127, 1, 1)
    subtract(128, 127, 1, 1)
    subtract(neg127, 127, 2, 1)
    subtract(127, 127, 0, 1)

    subtract(1, 127, alu.twos_complement_negation(126), 0)
    subtract(0, 127, neg127, 0)
    subtract(alu.twos_complement_negation(1), 127, neg128, 1)
    subtract(alu.twos_complement_negation(1), 127, 128, 1)

    # add or subtract 0 never carries
    subtract(5, 0, 5, 0)
    subtract(0, 0, 0, 0)
    subtract(alu.twos_complement_negation(5), 0, alu.twos_complement_negation(5), 0)

    # subtracting a negative number
    # carries iff going from negative to non-negative
    neg3 = alu.twos_complement_negation(3)
    subtract(5, neg3, 8, 0)
    subtract(2, neg3, 5, 0)
    subtract(0, neg3, 3, 0)
    subtract(alu.twos_complement_negation(1), neg3, 2, 1)
    subtract(neg3, neg3, 0, 1)
    subtract(alu.twos_complement_negation(4), neg3, alu.twos_complement_negation(1), 0)

    subtract(1, neg127, neg128, 0)
    subtract(1, neg127, 128, 0)
    subtract(0, neg127, 127, 0)
    subtract(alu.twos_complement_negation(1), neg127, 126, 1)

    subtract(1, neg128, 129, 0)
    subtract(1, neg128, neg127, 0)
    subtract(1, 128, 129, 0)
    subtract(1, 128, neg127, 0)
    subtract(0, neg128, neg128, 0)
    subtract(0, 128, neg128, 0)
    subtract(0, neg128, 128, 0)
    subtract(0, 128, 128, 0)
    subtract(alu.twos_complement_negation(1), neg128, 127, 1)
    subtract(alu.twos_complement_negation(1), 128, 127, 1)

    subtract(127, neg128, alu.twos_complement_negation(1), 0)
    subtract(neg128, neg128, 0, 1)
    subtract(neg127, neg128, 1, 1)
