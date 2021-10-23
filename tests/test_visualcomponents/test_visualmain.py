from typing import Any, Dict, Iterator
import pygame
from be8bbbce.computer import Computer
from be8bbbce.visualcomponents.visualmain import VisualMain
from tests.test_visualcomponents.patch_pygame import PatchedEvent
import threading
from time import sleep
import pytest


@pytest.fixture
def vm(patched_pygame_event: PatchedEvent) -> Iterator[VisualMain]:
    c = Computer(4, True)
    vm = VisualMain(c)
    run_thread = threading.Thread(None, lambda: vm.run())
    run_thread.start()
    yield vm
    patched_pygame_event.enqueue(patched_pygame_event.Event(pygame.QUIT, {}))
    run_thread.join(3)


def test_visualmain(patched_pygame_event: PatchedEvent) -> None:
    """
    race conditions could cause this test to fail
    because VisualMain and Computer are not programmed to be thread safe
    """
    c = Computer(4, True)
    vm = VisualMain(c)

    assert vm.paused
    assert vm.fps > 22

    run_thread = threading.Thread(None, lambda: vm.run())
    run_thread.start()

    try:
        def enq(event_type: int, attrs: Dict[str, Any]) -> None:
            """ enqueue an event and wait for the event to be processed """
            patched_pygame_event.enqueue(patched_pygame_event.Event(event_type, attrs))
            sleep(0.05)

        def press_key(key: int, hold: bool = False) -> None:
            """ `hold` simulates holding down the key for a repeated keydown signal """
            enq(pygame.KEYDOWN, {"key": key})
            if hold:
                enq(pygame.KEYDOWN, {"key": key})
            enq(pygame.KEYUP, {"key": key})

        enq(pygame.VIDEORESIZE, {"w": 300, "h": 200})
        small_led_size = vm.led_size
        small_font_size = vm.button_font.get_height()
        enq(pygame.VIDEORESIZE, {"w": 400, "h": 300})

        assert vm.led_size > small_led_size
        assert vm.button_font.get_height() > small_font_size

        press_key(pygame.K_p)

        assert not vm.paused

        press_key(pygame.K_c)

        assert not vm.paused

        press_key(pygame.K_SPACE)

        assert vm.paused

        press_key(pygame.K_SPACE, True)

        assert not vm.paused

        start_0 = vm.clock_count
        sleep(0.125)
        end_0 = vm.clock_count

        assert end_0 - start_0 > 3

        for _ in range(2):
            press_key(pygame.K_RIGHTBRACKET, True)
        start_1 = vm.clock_count
        sleep(0.125)
        end_1 = vm.clock_count

        assert end_1 - start_1 > 2.125 * (end_0 - start_0)

        for _ in range(4):
            press_key(pygame.K_LEFTBRACKET, True)
        start_2 = vm.clock_count
        sleep(0.125)
        end_2 = vm.clock_count

        assert end_2 - start_2 < 0.8 * (end_0 - start_0)

        down_count = 0
        while vm.clock_hz_exponent > 0 and down_count < 70:
            down_count += 1
            press_key(pygame.K_LEFTBRACKET)

        assert 0 < down_count < 61

        press_key(pygame.K_LEFTBRACKET)
        press_key(pygame.K_LEFTBRACKET)

        assert vm.clock_hz_exponent == 0

        up_count = 0
        previous_value = -1
        while vm.clock_hz_exponent != previous_value and up_count < 70:
            previous_value = vm.clock_hz_exponent
            up_count += 1
            press_key(pygame.K_RIGHTBRACKET)

        assert 65 > up_count > 9

        press_key(pygame.K_p)
        press_key(pygame.K_c)

        assert c.clock.value == 0

        enq(pygame.KEYDOWN, {"key": pygame.K_c})

        assert c.clock.value == 1

        enq(pygame.KEYDOWN, {"key": pygame.K_c})

        assert c.clock.value == 1

        enq(pygame.KEYUP, {"key": pygame.K_c})

        assert c.clock.value == 0

        prev_twos = vm.twos

        press_key(pygame.K_2)

        assert vm.twos != prev_twos

        press_key(pygame.K_2, True)

        assert vm.twos == prev_twos

        # just for the 100% coverage
        vm.draw_box_for_registers = True

        press_key(pygame.K_r)
        # still paused

        assert c.pc.value == 0

        # make sure holding down the reset button only resets it once
        enq(pygame.KEYDOWN, {"key": pygame.K_r})

        assert c.pc.value == 0

        c.pc.value = 14
        enq(pygame.KEYDOWN, {"key": pygame.K_r})

        assert c.pc.value == 14

        assert vm.pause_message_timer == 0

        press_key(pygame.K_o)

        assert vm.pause_message_timer > 0

    finally:
        patched_pygame_event.enqueue(patched_pygame_event.Event(pygame.QUIT, {}))
        run_thread.join(3)
