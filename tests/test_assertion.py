import pytest
from unittest.mock import AsyncMock, MagicMock
from src.engine.assertion_engine import AssertionEngine


@pytest.mark.asyncio
async def test_assert_text_present_success():
    page = MagicMock()
    page.inner_text = AsyncMock(return_value="Welcome to Dashboard - Account Overview")

    result = await AssertionEngine.evaluate(page, "text_present", "Dashboard")
    assert result["passed"] is True
    assert result["condition"] == "text_present"


@pytest.mark.asyncio
async def test_assert_text_present_failure():
    page = MagicMock()
    page.inner_text = AsyncMock(return_value="Error: 404 Page Not Found")

    result = await AssertionEngine.evaluate(page, "text_present", "Welcome")
    assert result["passed"] is False


@pytest.mark.asyncio
async def test_assert_url_contains():
    page = MagicMock()
    page.url = "https://example.com/checkout/success"

    result = await AssertionEngine.evaluate(page, "url_contains", "success")
    assert result["passed"] is True
