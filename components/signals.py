from typing import List
from components.receiver import Receiver


class Signals:
    # these could be anything (enum)
    # using the labels that he used
    # he started labeling signals here: https://youtu.be/Vw3uDOUJRGw?t=603
    HALT = "hlt"
    MAR_IN = "mi"
    RAM_IN = "ri"
    RAM_OUT = "ro"
    INSTR_OUT = "io"
    INSTR_IN = "ii"
    REG_A_IN = "ai"
    REG_A_OUT = "ao"
    ALU_OUT = "eo"
    SUBTRACT = "su"
    REG_B_IN = "bi"
    OUTPUT_IN = "oi"
    COUNTER_INCREMENT = "ce"  # enable
    COUNTER_OUT = "co"
    COUNTER_IN = "j"  # jump
    FLAGS_IN = "fi"

    REG_B_OUT = "bo"
    # B out not used (in original, ability to write to bus
    # is wired, but control signal is not connected to anything)

    CARRY_BIT = "cy"
    CLOCK = "clk"
    RESET = "rst"

    # Note that in the original computer some of these signals
    # are active low on the side of an inverter connected to the module.
    # In this emulator, they are all active high through the whole connection.

    def __init__(self):
        self.receivers: List[Receiver] = []

    def signal(self, code: str, value: int):
        """
        send signal to all receivers
        """
        # print("signal:", code, " value:", value)
        for receiver in self.receivers:
            receiver.receive_signal(code, value)

    def listen(self, receiver: Receiver):
        """
        make it so this receiver receives signals
        """
        self.receivers.append(receiver)
