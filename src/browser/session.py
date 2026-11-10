import os
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from src.config.settings import HarnessSettings


class BrowserSession:
    """Manages Playwright lifecycle, contexts, and page instances."""

    def __init__(self, settings: HarnessSettings):
        self.settings = settings
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    async def start(self) -> Page:
        """Launch browser and initialize isolated context and page."""
        self._playwright = await async_playwright().start()
        browser_type_name = self.settings.browser_type.lower()
        launcher = getattr(self._playwright, browser_type_name, self._playwright.chromium)

        self._browser = await launcher.launch(
            headless=self.settings.headless,
            slow_mo=self.settings.slow_mo_ms,
        )

        self._context = await self._browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-E2E-Harness/1.0",
        )
        self._context.set_default_timeout(self.settings.timeout_ms)

        self._page = await self._context.new_page()
        return self._page

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("Browser session has not been started. Call 'start()' first.")
        return self._page

    async def take_screenshot(self, name: str) -> Path:
        """Capture screenshot to configured report directory."""
        report_dir = self.settings.report_dir / "screenshots"
        report_dir.mkdir(parents=True, exist_ok=True)
        file_path = report_dir / f"{name}.png"
        await self.page.screenshot(path=str(file_path), full_page=True)
        return file_path

    async def close(self) -> None:
        """Gracefully release browser and playwright resources."""
        if self._context:
            await self._context.close()
            self._context = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        self._page = None
