from components.register import Register, RegisterIn, RegisterInOut, RegisterOut
from components.signals import Signals
from components.bus import Bus
from components.valueif import ValueInterface

LOAD = "LOAD"  # in
ENABLE = "ENABLE"  # out

def make_sure_load_works(reg: Register, bus: ValueInterface):
    bus.value = 42
    reg.receive_signal(LOAD, 1)
    reg.receive_signal(Signals.CLOCK, 1)
    reg.receive_signal(Signals.CLOCK, 0)

    assert reg.value == 42

def make_sure_load_does_not_work(reg: Register, bus: ValueInterface):
    bus.value = 42
    previous = reg.value
    reg.receive_signal(LOAD, 1)
    reg.receive_signal(Signals.CLOCK, 1)
    reg.receive_signal(Signals.CLOCK, 0)

    # Register that is not RegisterIn should not take value from bus
    assert reg.value == previous


def make_sure_enable_works(reg: Register, bus: ValueInterface):
    reg.value = 21
    reg.receive_signal(LOAD, 0)
    reg.receive_signal(ENABLE, 1)
    reg.receive_signal(Signals.CLOCK, 1)
    reg.receive_signal(Signals.CLOCK, 0)

    assert bus.value == 21

def make_sure_enable_does_not_work(reg: Register, bus: ValueInterface):
    reg.value = 21
    previous = bus.value
    reg.receive_signal(LOAD, 0)
    reg.receive_signal(ENABLE, 1)
    reg.receive_signal(Signals.CLOCK, 1)
    reg.receive_signal(Signals.CLOCK, 0)

    # Register that is not RegisterOut should not put value on bus
    assert bus.value == previous

def test_Register() -> None:
    signals = Signals()
    bus = Bus()
    reg = Register(signals, bus, LOAD, ENABLE)

    make_sure_load_does_not_work(reg, bus)
    make_sure_enable_does_not_work(reg, bus)

def test_RegisterIn() -> None:
    signals = Signals()
    bus = Bus()
    reg = RegisterIn(signals, bus, LOAD)

    make_sure_load_works(reg, bus)
    make_sure_enable_does_not_work(reg, bus)

def test_RegisterOut() -> None:
    signals = Signals()
    bus = Bus()
    reg = RegisterOut(signals, bus, ENABLE)

    make_sure_load_does_not_work(reg, bus)
    make_sure_enable_works(reg, bus)

def test_RegisterInOut() -> None:
    signals = Signals()
    bus = Bus()
    reg = RegisterInOut(signals, bus, LOAD, ENABLE)

    make_sure_load_works(reg, bus)
    make_sure_enable_works(reg, bus)

def test_register_reset() -> None:
    signals = Signals()
    bus = Bus()
    reg = Register(signals, bus, LOAD, ENABLE)

    reg.value = 17
    reg.receive_signal(LOAD, 1)
    reg.receive_signal(Signals.RESET, 0)

    assert reg.value == 17

    reg.receive_signal(Signals.RESET, 1)

    assert reg.value == 0
