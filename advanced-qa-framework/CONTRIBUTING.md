# 🤝 Contributing to Advanced QA Framework

Thank you for your interest in contributing to the **Advanced QA Framework** (`alok-kumar8765/advanced-qa-framework`)! To ensure smooth collaboration and maintain enterprise standards, please follow these guidelines when contributing code or reporting bugs.

---

## 🔄 Branching & Workflow Strategy

1. **Never commit directly to `main`.** The `main` branch is strictly reserved for stable, production-ready releases.
2. Create a feature or bugfix branch from `develop` (or `main`):
   * Feature branch naming: `feature/short-description` (e.g., `feature/add-oauth-fixtures`)
   * Bugfix branch naming: `fix/issue-description` (e.g., `fix/timeout-login-test`)
3. Submit a Pull Request (PR) against the `main` branch once your changes are fully tested.

---

## 💻 Local Development Setup

Before submitting code, ensure your local environment is fully synchronized and all tests pass:

1. Activate your virtual environment:
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux

```

2. Install latest dependencies:
```bash
pip install -r requirements.txt
playwright install

```


3. Run the full test suite locally:
```bash
pytest -v --browser chromium

```



---

## 🧪 Coding & Testing Standards

* **Page Object Model (POM):** All new page selectors and actions must reside inside the `pages/` directory. Never hardcode selectors directly inside test files.
* **Type Hinting:** Use Python type annotations across all new functions, methods, and classes.
* **Allure Reporting:** Ensure all test classes include proper `@allure.feature`, `@allure.story`, and `@allure.severity` decorators.
* **Data Decoupling:** Use external JSON files under `test_data/` for data-driven testing parameters.

---

## 🚀 Submitting a Pull Request

1. Ensure all existing and new tests pass successfully.
2. Verify that your code adheres to clean Python standards (PEP 8).
3. Push your branch to GitHub and open a Pull Request with a clear description of the changes introduced.


---

