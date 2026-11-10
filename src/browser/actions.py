import asyncio
from typing import Any, Dict
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


class BrowserActions:
    """Executes atomic browser actions with resilient selector resolution."""

    def __init__(self, page: Page):
        self.page = page

    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to a target URL."""
        try:
            await self.page.goto(url, wait_until="domcontentloaded")
            return {"status": "success", "url": self.page.url}
        except Exception as err:
            return {"status": "error", "message": f"Navigation failed: {str(err)}"}

    async def click(self, selector: str) -> Dict[str, Any]:
        """Click element by CSS, text, role, or testid selector."""
        try:
            locator = self._resolve_locator(selector)
            await locator.click(timeout=8000)
            return {"status": "success", "selector": selector}
        except PlaywrightTimeoutError:
            return {"status": "error", "message": f"Element '{selector}' timed out or not clickable."}
        except Exception as err:
            return {"status": "error", "message": f"Click failed on '{selector}': {str(err)}"}

    async def fill(self, selector: str, text: str) -> Dict[str, Any]:
        """Fill an input or textarea element with text."""
        try:
            locator = self._resolve_locator(selector)
            await locator.fill(text, timeout=8000)
            return {"status": "success", "selector": selector, "value": text}
        except PlaywrightTimeoutError:
            return {"status": "error", "message": f"Input '{selector}' timed out."}
        except Exception as err:
            return {"status": "error", "message": f"Fill failed on '{selector}': {str(err)}"}

    async def press_key(self, key: str) -> Dict[str, Any]:
        """Send a keyboard stroke (e.g. 'Enter', 'Tab', 'Escape')."""
        try:
            await self.page.keyboard.press(key)
            return {"status": "success", "key": key}
        except Exception as err:
            return {"status": "error", "message": f"Key press '{key}' failed: {str(err)}"}

    async def wait_seconds(self, seconds: float) -> Dict[str, Any]:
        """Pause execution to allow dynamic asynchronous rendering."""
        safe_delay = min(max(seconds, 0.1), 10.0)
        await asyncio.sleep(safe_delay)
        return {"status": "success", "waited": safe_delay}

    def _resolve_locator(self, selector: str):
        """Build resilient locator supporting text=, role=, or standard CSS."""
        selector_str = selector.strip()
        if selector_str.startswith("role="):
            role_name = selector_str.split("=", 1)[1]
            return self.page.get_by_role(role_name)
        if selector_str.startswith("text="):
            text_val = selector_str.split("=", 1)[1]
            return self.page.get_by_text(text_val, exact=False)
        return self.page.locator(selector_str).first
