from bus import Bus
from register import RegisterOut, Register, RegisterInOut
from receiver import Receiver
from signals import Signals


class ALU(RegisterOut):
    def __init__(self,
                 signals: Signals,
                 bus: Bus,
                 reg_a: Register,
                 reg_b: Register,
                 bit_count: int):
        super().__init__(signals, bus, Signals.ALU_OUT)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.max_plus_one = 1 << bit_count
        self.bit_count = bit_count
        self.carry = 0
        self.subtract = 0
        self.enabled = 0  # output to bus

    def twos_complement_negation(self, x):
        assert 0 <= x < self.max_plus_one
        x -= self.max_plus_one
        return 0 - x

    def add(self):
        # Register a and register b are unsigned integers.
        # The computer uses 2's complement to subtract, but only to subtract.
        # Nothing is ever interpreted in 2's complement.
        reg_b_value = self.reg_b.value
        if self.subtract:
            reg_b_value = self.twos_complement_negation(reg_b_value)
        self.value = self.reg_a.value + reg_b_value
        self.carry = 0
        if self.value >= self.max_plus_one:
            self.value %= self.max_plus_one
            self.carry = 1

        if self.enabled:
            # put result on bus again
            super().receive_signal(Signals.ALU_OUT, 1)

    def receive_signal(self, code: str, value: int):
        super().receive_signal(code, value)
        if code == Signals.CLOCK:
            # both clock going high and going low
            # in original computer, this is happening
            # constantly all the time and needs no signal
            self.add()
        elif code == Signals.SUBTRACT:
            self.subtract = value
            self.add()
        elif code == Signals.ALU_OUT:
            self.enabled = value


def test():
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
