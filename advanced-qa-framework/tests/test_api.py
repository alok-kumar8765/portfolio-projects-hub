import pytest
import allure
from core.api_client import APIClient

@allure.feature("Backend API Verification")
class TestAPIEndpoints:

    @pytest.fixture(autouse=True)
    def setup_client(self):
        self.api = APIClient()
        yield
        self.api.close()

    @allure.story("Check Application Health / Status")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_homepage_status_code(self):
        response = self.api.get("/")
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    @allure.story("Validate Unauthorized Access Protection & Redirect")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_secure_endpoint_requires_auth(self):
        # Hitting a protected route directly should redirect unauthenticated users to the login page
        response = self.api.get("/secure")
        assert response.status_code == 200
        # Verify it redirected to /login and displays the login heading
        assert "login" in str(response.url)
        assert "Login Page" in response.text