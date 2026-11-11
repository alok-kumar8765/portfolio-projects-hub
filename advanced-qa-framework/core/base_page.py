from playwright.sync_api import Page, TimeoutError
from core.logger import logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def click_with_self_healing(self, primary_selector: str, fallback_selector: str = None):
        """Self-healing click wrapper that falls back if primary selector fails."""
        try:
            logger.info(f"Attempting primary selector: {primary_selector}")
            self.page.locator(primary_selector).click(timeout=5000)
        except TimeoutError:
            if fallback_selector:
                logger.warning(f"Primary selector '{primary_selector}' failed. Self-healing to fallback: {fallback_selector}")
                self.page.locator(fallback_selector).click()
            else:
                raise

    def fill(self, selector: str, text: str):
        self.page.locator(selector).fill(text)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text().strip()

    def wait_for_selector(self, selector: str):
        self.page.locator(selector).wait_for(state="visible")