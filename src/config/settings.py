import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class HarnessSettings(BaseModel):
    """Central configuration for AI Web Test Harness."""

    ai_base_url: str = Field(
        default_factory=lambda: os.getenv("AI_BASE_URL", "https://api.deepseek.com/v1")
    )
    ai_api_key: str = Field(
        default_factory=lambda: os.getenv("AI_API_KEY", "")
    )
    ai_model_name: str = Field(
        default_factory=lambda: os.getenv("AI_MODEL_NAME", "deepseek-chat")
    )
    browser_type: str = Field(
        default_factory=lambda: os.getenv("BROWSER_TYPE", "chromium")
    )
    headless: bool = Field(
        default_factory=lambda: os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    )
    timeout_ms: int = Field(
        default_factory=lambda: int(os.getenv("TIMEOUT_MS", "30000"))
    )
    slow_mo_ms: int = Field(
        default_factory=lambda: int(os.getenv("SLOW_MO_MS", "0"))
    )
    max_agent_steps: int = Field(
        default_factory=lambda: int(os.getenv("MAX_AGENT_STEPS", "25"))
    )
    screenshot_on_failure: bool = Field(
        default_factory=lambda: os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() in ("true", "1", "yes")
    )
    report_dir: Path = Field(
        default_factory=lambda: Path(os.getenv("REPORT_DIR", "reports"))
    )


_SETTINGS_INSTANCE = None


def get_settings() -> HarnessSettings:
    """Retrieve cached singleton settings instance."""
    global _SETTINGS_INSTANCE
    if _SETTINGS_INSTANCE is None:
        _SETTINGS_INSTANCE = HarnessSettings()
    return _SETTINGS_INSTANCE
