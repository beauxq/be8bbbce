from components.instructionregister import InstructionRegister
from components.valueif import ValueInterface


class IRReader(ValueInterface):
    """ read 2 parts of instruction register separately """
    def __init__(self, ir: InstructionRegister):
        # not calling super().__init__ because value defined by getter
        # I can't find a good solution to this.
        # https://stackoverflow.com/questions/56493495/how-to-write-interface-contract-for-object-property-attribute-existence-in-p#
        self.ir = ir
        self.instruction_part = True

    @property
    def value(self):
        if self.instruction_part:
            return self.ir.value >> self.ir.address_length
        return self.ir.value % (1 << self.ir.address_length)
