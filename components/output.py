from components.register import RegisterIn
from components.signals import Signals
from components.bus import Bus


class Output(RegisterIn):
    def __init__(self, signals: Signals, bus: Bus, bit_count: int):
        super().__init__(signals, bus, Signals.OUTPUT_IN)
        # self.bit_count = bit_count
        self.max_plus_one = 1 << bit_count

    def unsigned_to_signed(self, x):
        half_max = self.max_plus_one // 2
        assert 0 <= x < self.max_plus_one
        if x >= half_max:
            return x - self.max_plus_one
        return x

    def print(self):
        print("        output:", hex(self.value), self.value,
              "(" + str(self.unsigned_to_signed(self.value)) + ")")

    def receive_signal(self, code: str, value: int):
        super().receive_signal(code, value)
        if (code == Signals.CLOCK) and value and self.load_set:
            self.print()
