from receiver import Receiver
from signals import Signals

from time import sleep


class Clock(Receiver):
    def __init__(self, signals: Signals):
        self.value = 0
        self.signals = signals
        self.signals.listen(self)  # clock listening to halt signal
        self.halted = 0

    def receive_signal(self, code: str, value: int):
        if code == Signals.HALT:
            self.halted = value

    def go_high(self):
        """ does nothing if clock is already high """
        if (not self.value) and (not self.halted):
            self.value = 1
            self.signals.signal(Signals.CLOCK, self.value)

    def go_low(self):
        """ does nothing if clock is already low """
        if (self.value) and (not self.halted):
            self.value = 0
            self.signals.signal(Signals.CLOCK, self.value)

    def go(self, cycles=8999999999999999999, delay_seconds=0):
        """ run clock the given number of cycles or until halt signal """
        delay_seconds /= 2
        while (cycles > 0) and (not self.halted):
            sleep(delay_seconds)
            self.go_high()
            sleep(delay_seconds)
            self.go_low()
            cycles -= 1
