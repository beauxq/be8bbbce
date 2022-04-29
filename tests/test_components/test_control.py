from typing import Counter
from be8bbbce.components.alu import ALU
from be8bbbce.components.bus import Bus
from be8bbbce.components.control import Control
from be8bbbce.asm import ASM, MICROCODE
from be8bbbce.components.receiver import Receiver
from be8bbbce.components.register import RegisterIn
from be8bbbce.components.signals import Signals
from be8bbbce.components.instructionregister import InstructionRegister
from be8bbbce.components.flags import Flags
import pytest


class ReceiverChecker(Receiver):
    def __init__(self) -> None:
        super().__init__()
        self.high_counter: Counter[str] = Counter()
        self.low_counter: Counter[str] = Counter()

    def receive_signal(self, code: str, value: int) -> None:
        if value:
            self.high_counter[code] += 1
        else:
            self.low_counter[code] += 1


@pytest.fixture
def control() -> Control:
    signals = Signals()
    bus = Bus()
    ir = InstructionRegister(signals, bus, 4)
    reg = RegisterIn(signals, bus, "x")
    alu = ALU(signals, bus, reg, reg, 8)
    flags = Flags(signals, alu)
    return Control(signals, ir, flags)


def test_microcode(control: Control) -> None:
    control.value = 0

    assert control.microcode() == Control.FETCH[0]

    control.execute()

    assert control.microcode() == Control.FETCH[1]

    control.ir.value = ASM.LDA << control.ir.address_length
    control.execute()

    assert control.microcode() == MICROCODE[ASM.LDA][0]

    def flags_in() -> None:
        control.flags.receive_signal(Signals.FLAGS_IN, 1)
        control.flags.receive_signal(Signals.CLOCK, 1)
        control.flags.receive_signal(Signals.CLOCK, 0)
        control.flags.receive_signal(Signals.FLAGS_IN, 0)

    # jump zero
    control.ir.value = ASM.JZ << control.ir.address_length
    control.flags.alu.value = 0
    control.flags.alu.carry = 0
    flags_in()

    assert control.microcode() == MICROCODE[ASM.JMP][0]

    control.flags.alu.value = 6
    control.flags.alu.carry = 0
    flags_in()

    assert control.microcode() == MICROCODE[ASM.NOP][0]

    # jump carry
    control.ir.value = ASM.JC << control.ir.address_length
    control.flags.alu.value = 0
    control.flags.alu.carry = 0
    flags_in()

    assert control.microcode() == MICROCODE[ASM.NOP][0]

    control.flags.alu.value = 6
    control.flags.alu.carry = 1
    flags_in()

    assert control.microcode() == MICROCODE[ASM.JMP][0]


def test_execute(control: Control) -> None:
    rec = ReceiverChecker()
    control.signals.listen(rec)

    control.value = 4

    control.execute()
    assert control.value == 0
    assert rec.high_counter[Signals.COUNTER_OUT] == 1
    assert rec.high_counter[Signals.MAR_IN] == 1

    control.execute()
    assert control.value == 1
    assert rec.low_counter[Signals.COUNTER_OUT] == 1
    assert rec.low_counter[Signals.MAR_IN] == 1
    assert rec.high_counter[Signals.RAM_OUT] == 1
    assert rec.high_counter[Signals.INSTR_IN] == 1
    assert rec.high_counter[Signals.COUNTER_INCREMENT] == 1

    control.execute()
    assert control.value == 2
    control.execute()
    assert control.value == 3
    control.execute()
    assert control.value == 4
    control.execute()
    assert control.value == 0

    control.ir.value = ASM.STA << control.ir.address_length
    control.execute()

    assert control.value == 1
    assert rec.high_counter[Signals.COUNTER_OUT] == 2
    assert rec.high_counter[Signals.MAR_IN] == 2
    assert rec.low_counter[Signals.COUNTER_OUT] == 2
    assert rec.low_counter[Signals.MAR_IN] == 2
    assert rec.high_counter[Signals.RAM_OUT] == 2
    assert rec.high_counter[Signals.INSTR_IN] == 2
    assert rec.high_counter[Signals.COUNTER_INCREMENT] == 2

    control.execute()

    assert control.value == 2
    assert rec.high_counter[Signals.INSTR_OUT] == 1
    assert rec.high_counter[Signals.MAR_IN] == 3

    control.execute()

    assert control.value == 3
    assert rec.high_counter[Signals.REG_A_OUT] == 1
    assert rec.high_counter[Signals.RAM_IN] == 1

    control.execute()
    assert control.value == 4
    control.execute()
    assert control.value == 0
    control.execute()
    assert control.value == 1


def test_receive_signal(control: Control) -> None:
    control.value = 0
    control.receive_signal(Signals.COUNTER_INCREMENT, 1)
    control.receive_signal(Signals.COUNTER_INCREMENT, 0)

    assert control.value == 0

    control.receive_signal(Signals.CLOCK, 1)

    assert control.value == 0

    control.receive_signal(Signals.CLOCK, 0)

    assert control.value == 1


def test_reset(control: Control) -> None:
    rec = ReceiverChecker()
    control.signals.listen(rec)

    control.ir.value = ASM.OUT << control.ir.address_length
    control.value = 1
    control.execute()

    assert rec.high_counter[Signals.REG_A_OUT] == 1
    assert rec.low_counter[Signals.REG_A_OUT] == 0

    print(control.microcode())
    control.reset()

    assert rec.low_counter[Signals.REG_A_OUT] == 1
    assert rec.high_counter[Signals.RESET] == 1
    assert control.value == 0
