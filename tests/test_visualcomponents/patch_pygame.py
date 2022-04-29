import pygame
from typing import Any, Deque, Dict, List, Union, Optional, Tuple, Iterable
import threading

import pytest


class PatchedSurface:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def blit(self,
             source: pygame.Surface,
             destination: Union[pygame.Rect, Tuple[int, int]]) -> None:
        pass

    def fill(self, color: Tuple[int, int, int]) -> None:
        pass

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, 0, 0)


def patched_rect(surface: pygame.Surface, color: Tuple[int, int, int], rect: pygame.Rect) -> None:
    pass


def patched_circle(surface: pygame.Surface,
                   color: Tuple[int, int, int],
                   center: Tuple[int, int],
                   radius: float) -> None:
    pass


def patched_set_mode(size: Tuple[int, int], flags: int) -> PatchedSurface:
    return PatchedSurface(size[0], size[1])


def patched_set_repeat(delay: int, interval: int) -> None:
    """ requires initialization of video system with `set_mode` """
    pass


def patched_flip() -> None:
    pass


class PatchedFont:
    def __init__(self, name: str, size: int) -> None:
        self.size = size

    def render(self,
               text: str,
               antialias: bool,
               color: Tuple[int, int, int],
               background: Optional[Tuple[int, int, int]] = None) -> PatchedSurface:
        return PatchedSurface(0, 0)

    def get_height(self) -> int:
        return self.size


class PatchedEvent:
    """
    instance of this in place of `pygame.event`

    with_threading means you run a pygame event loop in one thread while enqueuing events in another

    not with_threading means you queue up events, and then run your event loop

    without threading, it will always send pygame.QUIT if the queue is empty,
    so that your event loop doesn't run forever
    """
    class Event:
        """ in place of `pygame.event.Event` """
        def __init__(self, type: int, dict: Dict[str, Any]) -> None:
            self.type = type
            for k in dict:
                self.__setattr__(k, dict[k])

        def __repr__(self) -> str:
            return f"Event({self.type}, {str(self.__dict__)}"

    def __init__(self, with_threading: bool = False) -> None:
        self.q: Deque[List[Union[pygame.event.Event, "PatchedEvent.Event"]]] = Deque()
        self.lock = threading.Lock()
        self.with_threading = with_threading

    def get(self) -> Iterable[Union[pygame.event.Event, "PatchedEvent.Event"]]:
        to_return: Iterable[Union[pygame.event.Event, "PatchedEvent.Event"]] \
            = () if self.with_threading else (pygame.event.Event(pygame.QUIT, {}), )
        self.lock.acquire()
        if len(self.q):
            to_return = self.q.popleft()
        self.lock.release()

        return to_return

    def enqueue(self, events: Union[
        List[Union[pygame.event.Event, "PatchedEvent.Event"]],
        Union[pygame.event.Event, "PatchedEvent.Event"]
    ]) -> None:
        if not isinstance(events, list):
            events = [events]
        self.lock.acquire()
        self.q.append(events)
        self.lock.release()


def patch_pygame(monkeypatch: pytest.MonkeyPatch, with_threading: bool) -> PatchedEvent:
    """
    disables many of the parts of pygame that use a window

    with_threading means you run a pygame event loop in one thread while enqueuing events in another

    not with_threading means you queue up events, and then run your event loop

    without threading, it will always send pygame.QUIT if the queue is empty,
    so that your event loop doesn't run forever
    """
    monkeypatch.setattr(pygame.display, "set_mode", patched_set_mode)
    monkeypatch.setattr(pygame.draw, "rect", patched_rect)
    monkeypatch.setattr(pygame.draw, "circle", patched_circle)
    monkeypatch.setattr(pygame.key, "set_repeat", patched_set_repeat)
    monkeypatch.setattr(pygame.font, "Font", PatchedFont)
    patched_event = PatchedEvent(with_threading)
    monkeypatch.setattr(pygame, "event", patched_event)
    monkeypatch.setattr(pygame.display, "flip", patched_flip)

    return patched_event
