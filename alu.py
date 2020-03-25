from bus import Bus
from register import Register
from receiver import Receiver
from signals import Signals


class ALU(Receiver):
    def __init__(self,
                 bus: Bus,
                 signals: Signals,
                 reg_a: Register,
                 reg_b: Register,
                 bit_count: int):
        self.bus = bus
        signals.listen(self)
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.max_plus_one = 2 ** bit_count
        self.bit_count = bit_count
        self.value = 0
        self.carry = 0
        self.subtract = 0

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

    def receive_signal(self, code: str, value: int):
        if code == "clock":
            # both clock going high and going low
            # in original computer, this is happening
            # constantly all the time and needs no signal
            self.add()
        elif code == "e_out" and value == 1:
            self.bus.value = self.value
        elif code == "subtract":
            self.subtract = value


def test():
    signals = Signals()
    bus = Bus()
    reg_a = Register(signals, bus, "a_in", "a_out")
    reg_b = Register(signals, bus, "b_in", "b_out")
    alu = ALU(bus, signals, reg_a, reg_b, 8)

    reg_a.value = 6
    reg_b.value = 2
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 8
    assert alu.carry == 0

    reg_a.value = 125
    reg_b.value = 5
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 130
    assert alu.carry == 0

    reg_a.value = 250
    reg_b.value = 10
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 4
    assert alu.carry == 1

    reg_a.value = 10
    reg_b.value = 20
    alu.subtract = 1
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 246  # -10
    assert alu.carry == 0

    reg_a.value = 246  # -10
    reg_b.value = 20
    alu.subtract = 0
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 10
    assert alu.carry == 1

    reg_a.value = 10
    reg_b.value = 236  # -20
    alu.subtract = 0
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 246  # -10
    assert alu.carry == 0

    reg_a.value = 246  # -10
    reg_b.value = 236  # -20
    alu.subtract = 0
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 226  # -30
    assert alu.carry == 1

    reg_a.value = 246  # -10
    reg_b.value = 236  # -20
    alu.subtract = 1
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 10
    assert alu.carry == 1

    # below are the test cases Ben Eater spent time with in his videos

    reg_a.value = 0
    reg_b.value = 8
    alu.subtract = 0
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 8
    assert alu.carry == 0

    reg_a.value = 0
    reg_b.value = 8
    alu.subtract = 1
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 8+16+32+64+128
    assert alu.carry == 0

    reg_a.value = 64
    reg_b.value = 0
    alu.subtract = 0
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 64
    assert alu.carry == 0

    reg_a.value = 0
    reg_b.value = 4
    alu.subtract = 0
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 4
    assert alu.carry == 0

    reg_a.value = 6
    reg_b.value = 2
    alu.subtract = 1
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    assert alu.value == 4
    assert alu.carry == 1

    # move value from alu to reg a to keep counting down by 2
    signals.signal("e_out", 1)
    signals.signal("a_in", 1)
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    signals.signal("e_out", 0)
    signals.signal("a_in", 0)
    assert alu.value == 2
    assert alu.carry == 1

    signals.signal("e_out", 1)
    signals.signal("a_in", 1)
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    signals.signal("e_out", 0)
    signals.signal("a_in", 0)
    assert alu.value == 0
    assert alu.carry == 1

    signals.signal("e_out", 1)
    signals.signal("a_in", 1)
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    signals.signal("e_out", 0)
    signals.signal("a_in", 0)
    assert alu.value == 254
    assert alu.carry == 0

    signals.signal("e_out", 1)
    signals.signal("a_in", 1)
    signals.signal("clock", 1)
    signals.signal("clock", 0)
    signals.signal("e_out", 0)
    signals.signal("a_in", 0)
    assert alu.value == 252
    assert alu.carry == 1


if __name__ == "__main__":
    test()
