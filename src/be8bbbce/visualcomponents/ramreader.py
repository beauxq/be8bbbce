from be8bbbce.components.ram import Ram
from be8bbbce.components.valueif import ValueInterface


class RamReader(ValueInterface):
    """ ram doesn't have a value attribute for the visual to read """
    def __init__(self, ram: Ram):
        # not calling super().__init__ because value defined by getter
        # I can't find a good solution to this.
        # https://stackoverflow.com/questions/56493495/how-to-write-interface-contract-for-object-property-attribute-existence-in-p#
        self.ram = ram

    @property
    def value(self) -> int:
        return self.ram.memory[self.ram.mar.value]

    @value.setter
    def value(self, v: int) -> None:
        raise TypeError("no setter for RamReader value")
