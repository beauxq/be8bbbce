from signals import Signals
from clock import Clock
from register import RegisterInOut
from bus import Bus
from alu import ALU
from ram import Ram
from programcounter import ProgramCounter
from output import Output
from instructionregister import InstructionRegister
from flags import Flags
from control import Control

INSTRUCTION_LENGTH = 4


class Computer():
    def __init__(self, address_length: int):
        # One word can contain an instruction and an address.
        bit_count = INSTRUCTION_LENGTH + address_length
        # Some modules (registers, bus) don't need to know how many bits,
        # because they just use the Python int data structure for their values.

        self.signals = Signals()
        self.clock = Clock(self.signals)
        self.bus = Bus()
        self.reg_a = RegisterInOut(self.signals, self.bus,
                                   Signals.REG_A_IN, Signals.REG_A_OUT)
        self.reg_b = RegisterInOut(self.signals, self.bus,
                                   Signals.REG_B_IN, Signals.REG_B_OUT)
        # The ALU needs to know how many bits to emulate overflow accurately.
        self.alu = ALU(self.signals, self.bus,
                       self.reg_a, self.reg_b, bit_count)
        self.ram = Ram(self.signals, self.bus, address_length)
        self.pc = ProgramCounter(self.signals, self.bus, address_length)
        self.out = Output(self.signals, self.bus, bit_count)
        self.ir = InstructionRegister(self.signals, self.bus, address_length)
        self.flags = Flags(self.signals, self.alu)
        self.control = Control(self.signals, self.ir, self.flags)
