from be8bbbce.components.valueif import ValueInterface


class Bus(ValueInterface):
    def __init__(self):
        super().__init__()
        self.value = 0
