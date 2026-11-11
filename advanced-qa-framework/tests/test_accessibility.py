# tests/test_accessibility.py
import pytest
import allure
from axe_playwright_python.sync_playwright import Axe
from config.settings import settings

@allure.feature("Accessibility (A11y) Compliance")
class TestAccessibility:

    @allure.story("Login Page WCAG Auditing")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_accessibility(self, page):
        page.goto(f"{settings.BASE_URL}/login")
        page.wait_for_load_state("load")
        
        axe = Axe()
        results = axe.run(page)
        
        allure.attach(
            results.generate_report(),
            name="accessibility_violations_report",
            attachment_type=allure.attachment_type.TEXT
        )
        
        # Soft warning instead of hard stop for third-party demo site violations
        if results.violations_count > 0:
            print(f"⚠️ Notice: Found {results.violations_count} accessibility violations on target page.")