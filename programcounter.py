from receiver import Receiver
from signals import Signals
from bus import Bus


class ProgramCounter(Receiver):
    def __init__(self, signals: Signals, bus: Bus, address_length: int):
        signals.listen(self)
        self.bus = bus
        self.max_plus_one = 2 ** address_length
        self.value = 0
        self.pc_in = 0
        self.increment = 0

    def receive_signal(self, code: str, value: int):
        if code == Signals.COUNTER_IN:
            self.pc_in = value
        elif (code == Signals.COUNTER_OUT) and value:
            self.bus.value = self.value
        elif code == Signals.COUNTER_INCREMENT:
            self.increment = value
        elif (code == Signals.CLOCK) and value:
            if self.pc_in:
                self.value = self.bus.value
            if self.increment:
                self.value += 1
            self.value %= self.max_plus_one
