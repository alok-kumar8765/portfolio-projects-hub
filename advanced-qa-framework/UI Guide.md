# 🧭 TestOps Guide: Streamlit Control Dashboard & TestRail Integration

Welcome to the **Advanced QA Framework** TestOps documentation! This guide explains how to use our interactive web dashboard to run tests visually, and how automated test results are synced to TestRail for compliance and tracking.

---

## 📑 Table of Contents
1. [Introduction: Why Do We Need a Test Dashboard & TestRail?](#-introduction-why-do-we-need-a-test-dashboard--testrail)
2. [Part 1: Streamlit Control Dashboard](#-part-1-streamlit-control-dashboard)
   * What is it & how does it help?
   * How to set it up & run it
3. [Part 2: TestRail Integration & Credentials Setup](#-part-2-testrail-integration--credentials-setup)
   * What is it & how does it help?
   * Step-by-step for freshers: How to obtain and fill your credentials (`.env`)

---

## 💡 Introduction: Why Do We Need a Test Dashboard & TestRail?

* **Why a UI Dashboard (Streamlit)?** 
  Normally, QA engineers run tests via black-and-white terminal commands (`pytest`). For freshers, manual testers, or product managers, remembering complex CLI flags is difficult. The Streamlit dashboard provides a clean **point-and-click web interface** to select environments, pick test suites, trigger runs, and view live terminal logs instantly.
* **Why TestRail Integration?** 
  In an enterprise environment, tests cannot just pass or fail locally—they must be tracked against official business requirements and user stories. TestRail keeps our test cases centralized. By linking our framework, test execution results sync automatically without manual copy-pasting.

---

## 🖥️ Part 1: Streamlit Control Dashboard

### What This UI Gives You & How It Helps
* **Zero-Learning-Curve Execution:** Run tests without touching the terminal.
* **Environment Switching:** Instantly toggle between `dev` and `staging` profiles.
* **Live Monitoring:** Watch real-time test progress and view color-coded success/failure states.

### How to Run the Dashboard Locally
1. Ensure your virtual environment is active and dependencies are installed:
   ```bash
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
    ```

2. Launch the Streamlit application:

```bash
streamlit run dashboard/app.py

```


3. Streamlit will automatically open your default browser to `http://localhost:8501`.
4. Use the sidebar to pick your target environment, browser, and test suite, then click **▶️ Execute Selected Test Suite**.

---

## 🔑 Part 2: TestRail Integration & Credentials Setup

### What This Does

Whenever your test suite finishes running (either locally or in CI/CD), the `ReportingClient` (`core/reporting_client.py`) automatically connects to TestRail's API and logs whether tests passed or failed under the specified Test Run ID.

---

### 👶 Step-by-Step Guide for Freshers: How to Fill Your Credentials

If you are a new team member setting up your local environment for the first time, follow these exact steps to configure your TestRail credentials:

#### Step 1: Locate or Create Your `.env` File

In the root directory of your project (`advanced-qa-framework/`), look for a file named `.env`. If it does not exist, create a new file named `.env`.

#### Step 2: Obtain Your TestRail Credentials

1. **`TESTRAIL_URL`**: Log into your company's TestRail account (e.g., `https://yourcompany.testrail.io`). Copy that base URL.
2. **`TESTRAIL_USER`**: This is simply your company email address used to log into TestRail (e.g., `alok.kumar@company.com`).
3. **`TESTRAIL_APIKEY`**:
* In TestRail, click on your profile avatar in the top-right corner and go to **My Settings**.
* Navigate to the **API Keys** tab.
* Click **Add Key**, give it a name (e.g., `AutomationRunner`), and copy the generated key string. *(Note: TestRail requires an API key instead of your account password for security reasons).*


4. **`TESTRAIL_RUN_ID`**:
* Open TestRail and go to your **Test Runs & Results** section.
* Click on the specific active Test Run you want your automated results to report into.
* Look at your browser's address bar. The URL will look like `.../index.php?/runs/view/102`. The number at the very end (`102`) is your **Run ID**.



#### Step 3: Populate Your `.env` File

Open your `.env` file in your code editor (like VS Code) and paste your credentials like this:

```env
# Runtime Environment Settings
ENV=dev
BASE_URL=[https://the-internet.herokuapp.com](https://the-internet.herokuapp.com)
BROWSER=chromium
HEADLESS=true

# TestRail Configuration (Fill in your actual details below)
TESTRAIL_URL=[https://your-domain.testrail.io](https://your-domain.testrail.io)
TESTRAIL_USER=your-email@company.com
TESTRAIL_APIKEY=your_generated_api_key_here
TESTRAIL_RUN_ID=102

```

> ⚠️ **Important Security Warning:** Never commit your `.env` file to GitHub! It is already listed in `.gitignore` to keep your private API keys secure.

---
