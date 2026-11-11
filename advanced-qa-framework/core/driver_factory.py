from playwright.sync_api import Browser, Page
from config.settings import settings

class DriverFactory:
    @staticmethod
    def create_tracked_context(browser: Browser):
        """Creates an isolated browser context with video recording or tracing enabled if needed."""
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            record_video_dir="reports/videos/" if settings.ENV == "staging" else None
        )
        return context