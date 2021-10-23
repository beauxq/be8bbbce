from be8bbbce.components.instructionregister import InstructionRegister
from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus


def test_instructionregister() -> None:
    signals = Signals()
    bus = Bus()
    ir = InstructionRegister(signals, bus, 4)

    bus.value = (14 << ir.address_length) | 5
    signals.signal(Signals.INSTR_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.INSTR_IN, 0)

    assert ir.value == (14 << ir.address_length) | 5

    signals.signal(Signals.INSTR_OUT, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.INSTR_OUT, 0)

    assert bus.value == 5
