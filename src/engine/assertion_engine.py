from typing import Any, Dict
from playwright.async_api import Page


class AssertionEngine:
    """Evaluates declarative assertions against live Playwright page state."""

    @classmethod
    async def evaluate(cls, page: Page, condition_type: str, expected: str) -> Dict[str, Any]:
        """Run single assertion check."""
        try:
            if condition_type == "text_present":
                return await cls._assert_text_present(page, expected)
            if condition_type == "element_visible":
                return await cls._assert_element_visible(page, expected)
            if condition_type == "url_contains":
                return cls._assert_url_contains(page, expected)

            return {
                "passed": False,
                "error": f"Unsupported assertion condition: {condition_type}"
            }
        except Exception as err:
            return {"passed": False, "error": str(err)}

    @classmethod
    async def _assert_text_present(cls, page: Page, expected: str) -> Dict[str, Any]:
        body_text = await page.inner_text("body")
        passed = expected.lower() in body_text.lower()
        return {
            "passed": passed,
            "condition": "text_present",
            "expected": expected,
            "message": "Text found in body" if passed else "Text not present in page body"
        }

    @classmethod
    async def _assert_element_visible(cls, page: Page, selector: str) -> Dict[str, Any]:
        locator = page.locator(selector).first
        is_visible = await locator.is_visible()
        return {
            "passed": is_visible,
            "condition": "element_visible",
            "selector": selector,
            "message": "Element is visible" if is_visible else "Element is hidden or absent"
        }

    @classmethod
    def _assert_url_contains(cls, page: Page, expected_substring: str) -> Dict[str, Any]:
        current_url = page.url
        passed = expected_substring in current_url
        return {
            "passed": passed,
            "condition": "url_contains",
            "expected": expected_substring,
            "actual": current_url,
            "message": "URL matched expected pattern" if passed else "URL mismatch"
        }
