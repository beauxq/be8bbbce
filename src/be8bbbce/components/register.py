from be8bbbce.components.receiver import Receiver
from be8bbbce.components.signals import Signals
from be8bbbce.components.valueif import ValueInterface


class Register(ValueInterface, Receiver):
    """ base class for different types of registers """
    def __init__(self,
                 signals: Signals,
                 bus: ValueInterface,
                 my_load_signal: str,
                 my_enable_signal: str):
        super().__init__()
        self.signals = signals
        self.signals.listen(self)
        self.bus = bus
        # load is move data from bus to register (with clock pulse)
        self.my_load_signal = my_load_signal
        # enable is move data from register to bus
        self.my_enable_signal = my_enable_signal
        self.value = 0
        self.load_set = 0

    # implement these in subclasses
    def enable_out(self):
        pass

    def load_in(self):
        pass

    def receive_signal(self, code: str, value: int):
        if (code == self.my_enable_signal) and value:
            self.enable_out()
        elif code == self.my_load_signal:
            self.load_set = value
        elif (code == Signals.CLOCK) and value and self.load_set:
            # print("register", self.my_load_signal, "value", self.bus.value)
            self.load_in()
        elif (code == Signals.RESET) and value:
            self.value = 0
            self.load_set = 0


class RegisterIn(Register):
    """ register that can read from bus """
    def __init__(self,
                 signals: Signals,
                 bus: ValueInterface,
                 my_load_signal: str):
        super().__init__(signals, bus, my_load_signal, "x")

    def load_in(self):
        self.value = self.bus.value


class RegisterOut(Register):
    """ register that can write to bus """
    def __init__(self,
                 signals: Signals,
                 bus: ValueInterface,
                 my_enable_signal: str):
        super().__init__(signals, bus, "x", my_enable_signal)

    def enable_out(self):
        self.bus.value = self.value


class RegisterInOut(Register):
    """ register that can read from bus and write to bus """

    def load_in(self):
        self.value = self.bus.value

    def enable_out(self):
        self.bus.value = self.value
