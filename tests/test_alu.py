from components.signals import Signals
from components.bus import Bus
from components.register import RegisterInOut
from components.alu import ALU


def test() -> None:
    signals = Signals()
    bus = Bus()
    reg_a = RegisterInOut(signals, bus, Signals.REG_A_IN, Signals.REG_A_OUT)
    reg_b = RegisterInOut(signals, bus, Signals.REG_B_IN, Signals.REG_B_OUT)
    alu = ALU(signals, bus, reg_a, reg_b, 8)
    # TODO: test other bit lengths

    reg_a.value = 6
    reg_b.value = 2
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 8
    assert alu.carry == 0

    reg_a.value = 125
    reg_b.value = 5
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 130
    assert alu.carry == 0

    reg_a.value = 250
    reg_b.value = 10
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 4
    assert alu.carry == 1

    reg_a.value = 10
    reg_b.value = 20
    alu.subtract = 1
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 246  # -10
    assert alu.carry == 0

    reg_a.value = 10
    reg_b.value = 20
    signals.signal(Signals.SUBTRACT, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 246  # -10
    assert alu.carry == 0

    reg_a.value = 246  # -10
    reg_b.value = 20
    alu.subtract = 0
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 10
    assert alu.carry == 1

    reg_a.value = 10
    reg_b.value = 236  # -20
    alu.subtract = 0
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 246  # -10
    assert alu.carry == 0

    reg_a.value = 246  # -10
    reg_b.value = 236  # -20
    alu.subtract = 0
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 226  # -30
    assert alu.carry == 1

    reg_a.value = 246  # -10
    reg_b.value = 236  # -20
    alu.subtract = 1
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 10
    assert alu.carry == 1

    reg_a.value = 246  # -10
    reg_b.value = 236  # -20
    signals.signal(Signals.SUBTRACT, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 10
    assert alu.carry == 1

    # below are the test cases Ben Eater spent time with in his videos

    reg_a.value = 0
    reg_b.value = 8
    alu.subtract = 0
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 8
    assert alu.carry == 0

    reg_a.value = 0
    reg_b.value = 8
    alu.subtract = 1
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 8+16+32+64+128
    assert alu.carry == 0

    reg_a.value = 64
    reg_b.value = 0
    alu.subtract = 0
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 64
    assert alu.carry == 0

    reg_a.value = 0
    reg_b.value = 4
    alu.subtract = 0
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 4
    assert alu.carry == 0

    reg_a.value = 6
    reg_b.value = 2
    alu.subtract = 1
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    assert alu.value == 4
    assert alu.carry == 1

    # move value from alu to reg a to keep counting down by 2
    signals.signal(Signals.ALU_OUT, 1)
    signals.signal(Signals.REG_A_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.ALU_OUT, 0)
    signals.signal(Signals.REG_A_IN, 0)
    assert alu.value == 2
    assert alu.carry == 1

    signals.signal(Signals.ALU_OUT, 1)
    signals.signal(Signals.REG_A_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.ALU_OUT, 0)
    signals.signal(Signals.REG_A_IN, 0)
    assert alu.value == 0
    assert alu.carry == 1

    signals.signal(Signals.ALU_OUT, 1)
    signals.signal(Signals.REG_A_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.ALU_OUT, 0)
    signals.signal(Signals.REG_A_IN, 0)
    assert alu.value == 254
    assert alu.carry == 0

    signals.signal(Signals.ALU_OUT, 1)
    signals.signal(Signals.REG_A_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.ALU_OUT, 0)
    signals.signal(Signals.REG_A_IN, 0)
    assert alu.value == 252
    assert alu.carry == 1


if __name__ == "__main__":
    test()
