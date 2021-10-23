from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus
from be8bbbce.components.register import RegisterInOut


def test() -> None:
    signals = Signals()

    assert len(signals.receivers) == 0

    bus = Bus()
    reg = RegisterInOut(signals, bus, Signals.REG_A_IN, Signals.REG_A_OUT)

    assert len(signals.receivers) == 1

    bus.value = 3
    signals.signal(Signals.REG_A_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.REG_A_IN, 0)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)

    assert reg.value == 3

    reg.value = 5
    signals.signal(Signals.REG_A_OUT, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.REG_A_OUT, 0)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)

    assert bus.value == 5
