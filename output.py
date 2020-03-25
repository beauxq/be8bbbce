from receiver import Receiver
from signals import Signals
from bus import Bus


class Output(Receiver):
    def __init__(self, signals: Signals, bus: Bus, bit_count: int):
        signals.listen(self)
        self.bus = bus
        self.bit_count = bit_count
        self.value = 0
        self.load = 0

    def unsigned_to_signed(self, x):
        max_plus_one = 2 ** self.bit_count
        half_max = max_plus_one // 2
        assert 0 <= x < max_plus_one
        if x >= half_max:
            return x - max_plus_one
        return x

    def print(self):
        print("output:", hex(self.value), self.value,
              "(" + str(self.unsigned_to_signed(self.value)) + ")")

    def receive_signal(self, code: str, value: int):
        if code == Signals.OUTPUT_IN:
            self.load = value
        elif code == Signals.CLOCK:
            if self.load:
                self.value = self.bus.value
                self.print()
