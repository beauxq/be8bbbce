from receiver import Receiver
from typing import List


class Signals:
    # these could be anything (enum)
    # using the labels that he used
    # he started labeling signals here: https://youtu.be/Vw3uDOUJRGw?t=603
    HALT = "hlt"
    MAR_IN = "mi"
    RAM_OUT = "ro"
    RAM_IN = "ri"
    INSTR_OUT = "io"
    INSTR_IN = "ii"

    ALU_OUT = "eo"
    SUBTRACT = "su"

    CLOCK = "clk"

    def __init__(self):
        self.receivers: List[Receiver] = []

    def signal(self, code: str, value: int):
        print("signal:", code, " value:", value)
        for receiver in self.receivers:
            receiver.receive_signal(code, value)

    def listen(self, receiver: Receiver):
        self.receivers.append(receiver)
