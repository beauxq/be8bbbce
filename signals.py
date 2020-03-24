from receiver import Receiver
from typing import List


class Signals:
    def __init__(self):
        self.receivers: List[Receiver] = []

    def signal(self, code: str, value: int):
        print("signal:", code, " value:", value)
        for receiver in self.receivers:
            receiver.receive_signal(code, value)

    def listen(self, receiver: Receiver):
        self.receivers.append(receiver)
