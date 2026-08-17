import pytest

from app.config import get_settings


def test_configuration_rejects_cors_wildcard(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "*")
    get_settings.cache_clear()
    with pytest.raises(RuntimeError, match="CORS_ORIGINS"):
        get_settings()
    get_settings.cache_clear()


def test_configuration_rejects_documented_placeholder_secret(monkeypatch):
    monkeypatch.setenv(
        "SECRET_KEY",
        "remplacer-par-au-moins-32-caracteres-aleatoires",
    )
    get_settings.cache_clear()
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        get_settings()
    get_settings.cache_clear()
