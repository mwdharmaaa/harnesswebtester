import logging
from openai import AsyncOpenAI
from src.config.settings import HarnessSettings

logger = logging.getLogger(__name__)


def create_ai_client(settings: HarnessSettings) -> AsyncOpenAI:
    """Initialize AsyncOpenAI client with configured baseURL and API key.
    
    Supports DeepSeek (https://api.deepseek.com/v1), OpenCode Go,
    or any standard OpenAI-compatible gateway.
    """
    if not settings.ai_api_key:
        logger.warning("AI_API_KEY is unset. Ensure proper environment variables are provided.")

    return AsyncOpenAI(
        base_url=settings.ai_base_url,
        api_key=settings.ai_api_key or "sk-dummy-key",
        timeout=60.0,
        max_retries=2,
    )
