import pygame
from typing import Union, Optional, Tuple, Iterable

import pytest


class PatchedSurface:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def blit(self, source: pygame.Surface, destination: Union[pygame.Rect, Tuple[int, int]]):
        pass

    def fill(self, color: Tuple[int, int, int]):
        pass

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, 0, 0)


def patched_rect(surface: pygame.Surface, color: Tuple[int, int, int], rect: pygame.Rect):
    pass


def patched_circle(surface: pygame.Surface, color: Tuple[int, int, int], center: Tuple[int, int], radius: float):
    pass


def patched_set_mode(size: Tuple[int, int], flags: int) -> PatchedSurface:
    return PatchedSurface(size[0], size[1])


def patched_set_repeat(delay: int, interval: int):
    """ requires initialization of video system with `set_mode` """
    pass


def patched_flip() -> None:
    pass


class PatchedFont:
    def __init__(self, name: str, size: int) -> None:
        pass

    def render(self,
               text: str,
               antialias: bool,
               color: Tuple[int, int, int],
               background: Optional[Tuple[int, int, int]] = None) -> PatchedSurface:
        return PatchedSurface(0, 0)


def patched_event_get() -> Iterable[pygame.event.Event]:
    return ()


def patch_pygame(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(pygame.display, "set_mode", patched_set_mode)
    monkeypatch.setattr(pygame.draw, "rect", patched_rect)
    monkeypatch.setattr(pygame.draw, "circle", patched_circle)
    monkeypatch.setattr(pygame.key, "set_repeat", patched_set_repeat)
    monkeypatch.setattr(pygame.font, "Font", PatchedFont)
    monkeypatch.setattr(pygame.event, "get", patched_event_get)
    monkeypatch.setattr(pygame.display, "flip", patched_flip)
