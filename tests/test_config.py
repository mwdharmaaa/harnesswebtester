import os
from src.config.settings import HarnessSettings


def test_default_settings_instantiation():
    settings = HarnessSettings()
    assert settings.ai_model_name == "deepseek-chat"
    assert "deepseek" in settings.ai_base_url
    assert settings.browser_type == "chromium"
    assert settings.timeout_ms == 30000


def test_custom_environment_overrides(monkeypatch):
    monkeypatch.setenv("AI_MODEL_NAME", "deepseek-flash")
    monkeypatch.setenv("AI_BASE_URL", "https://api.opencode.go.id/v1")
    monkeypatch.setenv("HEADLESS", "false")
    monkeypatch.setenv("TIMEOUT_MS", "45000")

    settings = HarnessSettings()
    assert settings.ai_model_name == "deepseek-flash"
    assert settings.ai_base_url == "https://api.opencode.go.id/v1"
    assert settings.headless is False
    assert settings.timeout_ms == 45000
