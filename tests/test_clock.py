from components.clock import Clock
from components.receiver import Receiver
from components.signals import Signals


class ClockReceiver(Receiver):
    def __init__(self) -> None:
        super().__init__()
        self.high_counter = 0
        self.low_counter = 0
    
    def receive_signal(self, code: str, value: int):
        if code == Signals.CLOCK:
            if value == 1:
                self.high_counter += 1
            else:  # 0
                self.low_counter += 1


def test_clock_states() -> None:
    signals = Signals()
    clock = Clock(signals)
    
    assert clock.value == 0

    clock.go_high()

    assert clock.value == 1

    clock.go_low()

    assert clock.value == 0

    clock.toggle()

    assert clock.value == 1

    clock.toggle()

    assert clock.value == 0

    clock.toggle()
    clock.toggle()
    clock.toggle()

    assert clock.value == 1

    signals.signal(Signals.HALT, 1)
    signals.signal(Signals.HALT, 0)

    clock.toggle()

    assert clock.value == 1

    clock.go_low()

    assert clock.value == 1

    clock.go_high()

    assert clock.value == 1

    signals.signal(Signals.RESET, 1)
    signals.signal(Signals.RESET, 0)

    clock.go_low()

    assert clock.value == 0

    clock.toggle()

    assert clock.value == 1

    clock.toggle()

    assert clock.value == 0

    clock.go_high()

    assert clock.value == 1

    clock.toggle()
    clock.toggle()
    clock.toggle()
    clock.toggle()
    clock.toggle()

    assert clock.value == 0

    clock.go(7)

    assert clock.value == 0


def test_clock_sending_signals() -> None:
    signals = Signals()
    clock = Clock(signals)
    cr = ClockReceiver()
    signals.listen(cr)

    assert cr.high_counter == 0
    assert cr.low_counter == 0

    clock.go_high()

    assert cr.high_counter == 1
    assert cr.low_counter == 0

    clock.go_low()

    assert cr.high_counter == 1
    assert cr.low_counter == 1

    clock.toggle()

    assert cr.high_counter == 2
    assert cr.low_counter == 1

    clock.toggle()

    assert cr.high_counter == 2
    assert cr.low_counter == 2

    clock.toggle()
    clock.toggle()
    clock.toggle()

    assert cr.high_counter == 4
    assert cr.low_counter == 3

    clock.go(2929)

    # go always starts with go_high even if it's already high
    assert cr.high_counter == 2932
    assert cr.low_counter == 2932
