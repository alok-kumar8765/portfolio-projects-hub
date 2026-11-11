import pytest
import allure
import os
import requests
import pytest
from core.reporting_client import ReportingClient

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Retrieve page fixture safely from the test function args if available
        page = item.funcargs.get("page", None)
        if page:
            screenshot_bytes = page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Sends automated build execution report card to Slack webhook."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return

    passed_count = session.testsfailed
    status_text = "❌ Test Suite Failed" if exitstatus != 0 else "✅ Test Suite Passed Successfully"
    
    payload = {
        "text": f"*Enterprise QA Pipeline Completed*\nStatus: {status_text}\nEnvironment: {os.getenv('ENV', 'dev')}"
    }
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to dispatch Slack notification: {e}")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Syncs test results to TestRail/Jira upon test run completion."""
    reporter = ReportingClient()
    
    # Determine overall status and push summary
    status_msg = "Automated test run completed successfully." if exitstatus == 0 else "Automated test run completed with failures."
    
    # Example: Syncing a generic suite run status if integration is enabled
    # You can also parse individual test node IDs to map against specific TestRail Case IDs
    print(f"[Reporting Hook] {status_msg}")