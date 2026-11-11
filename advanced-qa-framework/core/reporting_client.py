import os
import httpx
from core.logger import logger

class ReportingClient:
    def __init__(self):
        self.testrail_url = os.getenv("TESTRAIL_URL", "")
        self.testrail_user = os.getenv("TESTRAIL_USER", "")
        self.testrail_apikey = os.getenv("TESTRAIL_APIKEY", "")
        self.run_id = os.getenv("TESTRAIL_RUN_ID", "1")

    def push_test_result(self, case_id: int, status_id: int, comment: str = ""):
        """
        Pushes automated test execution results to TestRail.
        status_id: 1 = Passed, 5 = Failed, 2 = Blocked
        """
        if not self.testrail_url or not self.testrail_apikey:
            logger.warning("TestRail credentials not configured. Skipping remote result push.")
            return

        endpoint = f"{self.testrail_url}/index.php?/api/v2/add_result_for_case/{self.run_id}/{case_id}"
        payload = {
            "status_id": status_id,
            "comment": comment
        }
        
        try:
            response = httpx.post(
                endpoint,
                json=payload,
                auth=(self.testrail_user, self.testrail_apikey),
                timeout=10.0
            )
            if response.status_code == 200:
                logger.info(f"Successfully synced Case C{case_id} status ({status_id}) to TestRail.")
            else:
                logger.error(f"Failed to push result to TestRail: {response.text}")
        except Exception as e:
            logger.error(f"Exception occurred while communicating with TestRail API: {e}")