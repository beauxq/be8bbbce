from be8bbbce.components.register import RegisterIn
from be8bbbce.components.signals import Signals
from be8bbbce.components.bus import Bus


class Output(RegisterIn):
    def __init__(self, signals: Signals, bus: Bus, bit_count: int) -> None:
        super().__init__(signals, bus, Signals.OUTPUT_IN)
        # self.bit_count = bit_count
        self.max_plus_one = 1 << bit_count

    def unsigned_to_signed(self, x: int) -> int:
        half_max = self.max_plus_one // 2
        assert 0 <= x < self.max_plus_one
        if x >= half_max:
            return x - self.max_plus_one
        return x

    def print(self) -> None:
        print("        output:", hex(self.value), self.value,
              "(" + str(self.unsigned_to_signed(self.value)) + ")")

    def receive_signal(self, code: str, value: int) -> None:
        super().receive_signal(code, value)
        if (code == Signals.CLOCK) and value and self.load_set:
            self.print()
