from components.ram import Ram
from components.signals import Signals
from components.bus import Bus


def test_ram() -> None:
    signals = Signals()
    bus = Bus()
    ram = Ram(signals, bus, 4, 8, True)

    def signal_with_clock(signal: str) -> None:
        signals.signal(signal, 1)
        signals.signal(Signals.CLOCK, 1)
        signals.signal(Signals.CLOCK, 0)
        signals.signal(signal, 0)

    assert len(ram.memory) == 16

    # test initialized memory to 0
    assert ram.memory.count(0) == 16

    bus.value = 64 + 7
    signal_with_clock(Signals.MAR_IN)

    # more significant bits don't go in mar
    assert ram.mar.value == 7

    signal_with_clock(Signals.RAM_IN)

    assert ram.memory[7] == 64 + 7

    bus.value = 2
    signal_with_clock(Signals.MAR_IN)
    signal_with_clock(Signals.RAM_OUT)

    assert bus.value == 0

    ram2 = Ram(signals, bus, 4, 8, False)

    assert len(ram.memory) == 16

    # test random initialization
    # probability of this test failing is 1 / 1e38
    assert ram2.memory.count(0) < 16
