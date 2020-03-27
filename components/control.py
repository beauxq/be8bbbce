from components.receiver import Receiver
from components.signals import Signals
from components.instructionregister import InstructionRegister
from components.flags import Flags
from asm import ASM, MICROCODE


class Control(Receiver):
    FETCH = (
        (Signals.COUNTER_OUT, Signals.MAR_IN),
        (Signals.RAM_OUT, Signals.INSTR_IN, Signals.COUNTER_INCREMENT),
    )

    def __init__(self,
                 signals: Signals,
                 ir: InstructionRegister,
                 flags: Flags):
        self.signals = signals
        self.signals.listen(self)
        self.ir = ir
        self.flags = flags
        self.step = 0

    def microcode(self):
        if self.step < 2:
            return Control.FETCH[self.step]

        instruction = self.ir.value >> self.ir.address_length

        # conditional jump is either JMP or NOP
        if instruction == ASM.JC:
            instruction = ASM.JMP if self.flags.get_carry() else ASM.NOP
        elif instruction == ASM.JZ:
            instruction = ASM.JMP if self.flags.get_zero() else ASM.NOP

        return MICROCODE[instruction][self.step - 2]

    def execute(self):
        # turn off last control word
        for signal in self.microcode():
            self.signals.signal(signal, 0)

        # increment to next control word
        self.step = (self.step + 1) % 5
        # 5 microinstructions for each instruction

        # debug message
        """
        instruction = self.ir.value >> self.ir.address_length
        if self.step == 2:
            print("found instruction:", ASM(instruction),
                  self.ir.value % (1 << self.ir.address_length))
        """

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

    def reset(self):
        self.signals.signal(Signals.RESET, 1)
        self.step = 4  # last step
        self.execute()
