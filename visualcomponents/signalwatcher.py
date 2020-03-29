from components.receiver import Receiver
from components.signals import Signals

signal_to_bit = {
    Signals.HALT: 1 << 15,
    Signals.MAR_IN: 1 << 14,
    Signals.RAM_IN: 1 << 13,
    Signals.RAM_OUT: 1 << 12,
    Signals.INSTR_OUT: 1 << 11,
    Signals.INSTR_IN: 1 << 10,
    Signals.REG_A_IN: 1 << 9,
    Signals.REG_A_OUT: 1 << 8,
    Signals.ALU_OUT: 1 << 7,
    Signals.SUBTRACT: 1 << 6,
    Signals.REG_B_IN: 1 << 5,
    Signals.OUTPUT_IN: 1 << 4,
    Signals.COUNTER_INCREMENT: 1 << 3,
    Signals.COUNTER_OUT: 1 << 2,
    Signals.COUNTER_IN: 1 << 1,
    Signals.FLAGS_IN: 1 << 0
}


class SignalWatcher(Receiver):
    def __init__(self, signals: Signals):
        signals.listen(self)
        self.value = 0

    def receive_signal(self, code: str, value: int):
        if code in signal_to_bit:
            bit = signal_to_bit[code]
            if value:
                self.value |= bit
            else:  # signal off
                self.value &= ~bit
        elif code == Signals.RESET:
            self.value = 0
