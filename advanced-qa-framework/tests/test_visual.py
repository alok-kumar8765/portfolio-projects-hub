import pytest
import allure
from config.settings import settings

@allure.feature("Visual Regression & UI Artifacts")
class TestVisualRegression:

    @allure.story("Capture Login Page Visual Snapshot")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_visual_snapshot(self, page):
        # Navigate to the login page
        page.goto(f"{settings.BASE_URL}/login")
        
        # Ensure fonts and layout are fully settled before capture
        page.wait_for_load_state("networkidle")
        
        # Capture full-page screenshot
        screenshot_bytes = page.screenshot(full_page=True)
        
        # Attach the screenshot directly to the Allure report for visual code reviews
        allure.attach(
            screenshot_bytes,
            name="login_page_visual_render",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Basic assertion to verify page integrity
        assert "login" in page.url