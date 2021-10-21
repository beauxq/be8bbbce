from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus
from be8bbbce.components.register import RegisterInOut
from be8bbbce.components.alu import ALU


def test_twos_complement() -> None:
    signals = Signals()
    bus = Bus()
    reg_a = RegisterInOut(signals, bus, Signals.REG_A_IN, Signals.REG_A_OUT)
    reg_b = RegisterInOut(signals, bus, Signals.REG_B_IN, Signals.REG_B_OUT)
    alu = ALU(signals, bus, reg_a, reg_b, 8)

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


def test_arithmetic() -> None:
    signals = Signals()
    bus = Bus()
    reg_a = RegisterInOut(signals, bus, Signals.REG_A_IN, Signals.REG_A_OUT)
    reg_b = RegisterInOut(signals, bus, Signals.REG_B_IN, Signals.REG_B_OUT)
    alu = ALU(signals, bus, reg_a, reg_b, 8)
    # TODO: test other bit lengths

    def arithmetic(a: int, b: int, result: int, carry: int, subtract: int):
        # set subtract input directly
        reg_a.value = a
        reg_b.value = b
        alu.subtract = subtract
        signals.signal(Signals.CLOCK, 1)
        signals.signal(Signals.CLOCK, 0)
        assert alu.value == result
        assert alu.carry == carry

        # send subtract signal
        reg_a.value = a
        reg_b.value = b
        signals.signal(Signals.SUBTRACT, subtract)
        signals.signal(Signals.CLOCK, 1)
        signals.signal(Signals.CLOCK, 0)
        assert alu.value == result
        assert alu.carry == carry

    def add(a: int, b: int, result: int, carry: int):
        arithmetic(a, b, result, carry, 0)
    
    def subtract(a: int, b: int, result: int, carry: int):
        arithmetic(a, b, result, carry, 1)

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
    
    subtract(0, 8, 8+16+32+64+128, 0)
    subtract(0, 8, alu.twos_complement_negation(8), 0)

    add(64, 0, 64, 0)

    add(0, 4, 4, 0)

    subtract(6, 2, 4, 1)

    def alu_to_a() -> None:
        """
        move value from alu to reg a to keep counting down by 2
        """
        signals.signal(Signals.ALU_OUT, 1)
        signals.signal(Signals.REG_A_IN, 1)
        signals.signal(Signals.CLOCK, 1)
        signals.signal(Signals.CLOCK, 0)
        signals.signal(Signals.ALU_OUT, 0)
        signals.signal(Signals.REG_A_IN, 0)
    
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
