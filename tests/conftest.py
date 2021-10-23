import pytest
from tests.test_visualcomponents.patch_pygame import PatchedEvent, patch_pygame as _patch_pygame


@pytest.fixture
def patched_pygame_event(monkeypatch: pytest.MonkeyPatch) -> PatchedEvent:
    return _patch_pygame(monkeypatch, True)
