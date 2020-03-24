from receiver import Receiver
from bus import Bus
from signals import Signals


class Register(Receiver):
    def __init__(self,
                 signals: Signals,
                 bus: Bus,
                 my_load_signal: str,
                 my_enable_signal: str):
        self.signals = signals
        self.signals.listen(self)
        self.bus = bus
        self.my_load_signal = my_load_signal
        self.my_enable_signal = my_enable_signal
        self.value = 0
        self.load_set = 0

    def receive_signal(self, code: str, value: int):
        if code == self.my_enable_signal and value:
            self.bus.value = self.value
        elif code == self.my_load_signal:
            self.load_set = value
        elif code == "clock" and value and self.load_set:
            self.value = self.bus.value
