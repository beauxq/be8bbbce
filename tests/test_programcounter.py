from be8bbbce.components.programcounter import ProgramCounter
from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus


def test_programcounter() -> None:
    signals = Signals()
    bus = Bus()
    pc = ProgramCounter(signals, bus, 4)

    signals.signal(Signals.RESET, 1)
    signals.signal(Signals.RESET, 0)

    assert pc.value == 0

    def signal_with_clock(signal: str) -> None:
        signals.signal(signal, 1)
        signals.signal(Signals.CLOCK, 1)
        signals.signal(Signals.CLOCK, 0)
        signals.signal(signal, 0)
    
    signal_with_clock(Signals.COUNTER_INCREMENT)

    assert pc.value == 1
    
    signal_with_clock(Signals.COUNTER_INCREMENT)

    assert pc.value == 2

    signal_with_clock(Signals.COUNTER_OUT)

    assert bus.value == 2

    bus.value = 14

    signal_with_clock(Signals.COUNTER_IN)

    assert pc.value == 14
    
    signal_with_clock(Signals.COUNTER_INCREMENT)

    assert pc.value == 15
    
    signal_with_clock(Signals.COUNTER_INCREMENT)

    assert pc.value == 0
