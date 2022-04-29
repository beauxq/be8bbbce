from be8bbbce.components.alu import ALU
from be8bbbce.components.bus import Bus
from be8bbbce.components.flags import Flags
from be8bbbce.components.register import Register
from be8bbbce.components.signals import Signals


def test_flags() -> None:
    signals = Signals()
    bus = Bus()
    reg = Register(signals, bus, "x", "x")
    alu = ALU(signals, bus, reg, reg, 8)
    flags = Flags(signals, alu)

    def alu_value_to_flags(alu_v: int, alu_c: int, expected_z: int, expected_c: int) -> None:
        alu.value = alu_v
        alu.carry = alu_c
        flags.receive_signal(Signals.FLAGS_IN, 1)
        flags.receive_signal(Signals.CLOCK, 1)
        flags.receive_signal(Signals.CLOCK, 0)

        assert flags.get_carry() == expected_c
        assert flags.get_zero() == expected_z

    alu_value_to_flags(0, 0, 1, 0)
    alu_value_to_flags(28, 0, 0, 0)
    alu_value_to_flags(0, 1, 1, 1)
    alu_value_to_flags(201, 1, 0, 1)
