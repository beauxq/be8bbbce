from receiver import Receiver
from signals import Signals
from instructionregister import InstructionRegister
from asm import ASM, MICROCODE


class Control(Receiver):
    FETCH = (
        (Signals.COUNTER_OUT, Signals.MAR_IN),
        (Signals.RAM_OUT, Signals.INSTR_IN, Signals.COUNTER_INCREMENT),
    )

    def __init__(self, signals: Signals, ir: InstructionRegister):
        self.signals = signals
        self.signals.listen(self)
        self.ir = ir
        self.step = 0

    def microcode(self):
        if self.step < 2:
            return Control.FETCH[self.step]

        instruction = self.ir.value >> self.ir.address_length
        return MICROCODE[instruction][self.step - 2]

    def execute(self):
        # turn off last control word
        for signal in self.microcode():
            self.signals.signal(signal, 0)

        # increment to next control word
        self.step = (self.step + 1) % 5
        # 5 microinstructions for each instruction

        # debug message
        instruction = self.ir.value >> self.ir.address_length
        if self.step == 2:
            print("found instruction:", ASM(instruction))

        # turn on current control word
        for signal in self.microcode():
            self.signals.signal(signal, 1)

    def receive_signal(self, code: str, value: int):
        if code == Signals.CLOCK:
            if value:
                # high clock
                pass
            else:
                # low clock
                self.execute()
