import httpx
from config.settings import settings
from core.logger import logger

class APIClient:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0, follow_redirects=True)

    def get(self, endpoint: str, headers: dict = None):
        logger.info(f"API GET request to: {endpoint}")
        response = self.client.get(endpoint, headers=headers)
        logger.info(f"API Response Status: {response.status_code}")
        return response

    def post(self, endpoint: str, data: dict = None, json_data: dict = None, headers: dict = None):
        logger.info(f"API POST request to: {endpoint}")
        response = self.client.post(endpoint, data=data, json=json_data, headers=headers)
        logger.info(f"API Response Status: {response.status_code}")
        return response

    def close(self):
        self.client.close()