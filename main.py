from signals import Signals
from clock import Clock


class Computer():
    def __init__(self):
        self.signals = Signals()
        self.clock = Clock(self.signals)


def main():
    computer = Computer()
    computer.clock.go_high()
    computer.clock.go_low()


if __name__ == "__main__":
    main()
