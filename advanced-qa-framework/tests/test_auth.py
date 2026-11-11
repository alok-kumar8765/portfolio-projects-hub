import json
import os
import pytest
import allure
from pages.login_page import LoginPage
from config.settings import settings
from core.logger import logger

# Helper function to load test data safely
def load_test_data(file_path: str):
    full_path = os.path.join(os.path.dirname(__file__), "..", file_path)
    with open(full_path, "r") as f:
        return json.load(f)["login_scenarios"]

@allure.feature("Authentication Service - Data-Driven Testing")
class TestDataDrivenAuthentication:

    @allure.story("Parameterized Login Scenarios")
    @pytest.mark.parametrize("scenario", load_test_data("test_data/login_data.json"))
    def test_login_matrix(self, page, scenario):
        logger.info(f"Executing test scenario: {scenario['test_id']} with user: {scenario['username']}")
        
        login_page = LoginPage(page)
        login_page.navigate(f"{settings.BASE_URL}/login")
        
        # Perform login using externalized data
        login_page.login(scenario["username"], scenario["password"])
        
        # Assert outcome based on expectation flag
        if scenario["is_success"]:
            assert scenario["expected_url_part"] in page.url
            flash_text = login_page.get_flash_message()
            assert scenario["expected_message"] in flash_text
        else:
            flash_text = login_page.get_flash_message()
            assert scenario["expected_message"] in flash_text