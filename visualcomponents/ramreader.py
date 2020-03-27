from components.ram import Ram


class RamReader:
    """ ram doesn't have a value attribute for the visual to read """
    def __init__(self, ram: Ram):
        self.ram = ram

    @property
    def value(self):
        return self.ram.memory[self.ram.mar.value]
