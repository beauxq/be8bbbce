from receiver import Receiver
from signals import Signals


class Clock(Receiver):
    def __init__(self, signals: Signals):
        self.value = 0
        self.signals = signals
        self.signals.listen(self)  # clock listening to halt signal
        self.halted = 0

    def receive_signal(self, code: str, value: int):
        if code == "halt":
            self.halted = value

    def go_high(self):
        if not self.halted:
            self.value = 1
            self.signals.signal("clock", self.value)

    def go_low(self):
        if not self.halted:
            self.value = 0
            self.signals.signal("clock", self.value)
