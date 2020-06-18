from components.receiver import Receiver
from components.signals import Signals
from components.instructionregister import InstructionRegister
from components.flags import Flags
from asm import ASM, MICROCODE


class Control(Receiver):
    OUT_SIGNALS = {  # all the signals that put something on the bus
        Signals.RAM_OUT,
        Signals.INSTR_OUT,
        Signals.REG_A_OUT,
        Signals.ALU_OUT,
        Signals.COUNTER_OUT,
        Signals.REG_B_OUT
    }
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
        self.value = 0  # microcode step

    def microcode(self):
        if self.value < 2:
            return Control.FETCH[self.value]

        instruction = self.ir.value >> self.ir.address_length

        # conditional jump is either JMP or NOP
        if instruction == ASM.JC:
            instruction = ASM.JMP if self.flags.get_carry() else ASM.NOP
        elif instruction == ASM.JZ:
            instruction = ASM.JMP if self.flags.get_zero() else ASM.NOP

        return MICROCODE[instruction][self.value - 2]

    def turn_off_current_signals(self):
        for signal in self.microcode():
            self.signals.signal(signal, 0)

    def execute(self):
        # turn off last control word
        self.turn_off_current_signals()

        # increment to next control word
        self.value = (self.value + 1) % 5
        # 5 microinstructions for each instruction

        # debug message
        """
        instruction = self.ir.value >> self.ir.address_length
        if self.step == 2:
            print("found instruction:", ASM(instruction),
                  self.ir.value % (1 << self.ir.address_length))
        """

        # turn on current control word
        anything_out = False
        for signal in self.microcode():
            self.signals.signal(signal, 1)
            if signal in Control.OUT_SIGNALS:
                anything_out = True
        # if nothing sent to bus, clear bus
        if not anything_out:
            self.ir.bus.value = 0

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
        self.turn_off_current_signals()
        self.value = 4  # last step
        self.execute()
