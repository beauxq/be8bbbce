import pytest
from tests.test_visualcomponents.patch_pygame import patch_pygame as _patch_pygame


@pytest.fixture
def patch_pygame(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_pygame(monkeypatch)
