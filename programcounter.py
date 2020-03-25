from register import RegisterInOut
from signals import Signals
from bus import Bus


class ProgramCounter(RegisterInOut):
    def __init__(self, signals: Signals, bus: Bus, address_length: int):
        super().__init__(signals, bus, Signals.COUNTER_IN, Signals.COUNTER_OUT)
        self.max_plus_one = 1 << address_length
        self.increment = 0

    def receive_signal(self, code: str, value: int):
        super().receive_signal(code, value)
        if code == Signals.COUNTER_INCREMENT:
            self.increment = value
        elif (code == Signals.CLOCK) and value:
            if self.increment:
                self.value += 1
        self.value %= self.max_plus_one
