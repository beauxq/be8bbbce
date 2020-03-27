from components.instructionregister import InstructionRegister


class IRReader:
    """ read 2 parts of instruction register separately """
    def __init__(self, ir: InstructionRegister):
        self.ir = ir
        self.instruction_part = True

    @property
    def value(self):
        if self.instruction_part:
            return self.ir.value >> self.ir.address_length
        return self.ir.value % (1 << self.ir.address_length)
