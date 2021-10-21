from be8bbbce.components.output import Output
from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus
import _pytest.capture


def test_u2s() -> None:
    signals = Signals()
    bus = Bus()
    out = Output(signals, bus, 8)

    for i in range(128):
        assert out.unsigned_to_signed(i) == i
        assert out.unsigned_to_signed(i + 128) == i - 128

def test_output(capsys: _pytest.capture.CaptureFixture[str]) -> None:
    signals = Signals()
    bus = Bus()
    Output(signals, bus, 8)

    bus.value = 77
    signals.signal(Signals.OUTPUT_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.OUTPUT_IN, 0)
    printed = capsys.readouterr()

    assert "77" in printed.out

    bus.value = 130
    signals.signal(Signals.OUTPUT_IN, 1)
    signals.signal(Signals.CLOCK, 1)
    signals.signal(Signals.CLOCK, 0)
    signals.signal(Signals.OUTPUT_IN, 0)
    printed = capsys.readouterr()

    assert "130" in printed.out
    # two's complement
    assert "-126" in printed.out
    