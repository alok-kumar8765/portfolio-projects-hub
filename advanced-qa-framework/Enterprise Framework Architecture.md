advanced-qa-framework/
│
├── config/
│   ├── __init__.py
│   ├── settings.py            # Pydantic-based environment config
│   └── environments/
│       ├── dev.env
│       └── staging.env
│
├── core/
│   ├── __init__.py
│   ├── driver_factory.py      # Browser lifecycle management
│   ├── base_page.py           # Explicit waits, logging, wrapper methods
│   └── logger.py              # Structured JSON / Console logging
│
├── pages/
│   ├── __init__.py
│   └── login_page.py          # Page Object Model implementation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Global Pytest fixtures, hooks, screenshots
│   └── test_auth.py           # Test suites
│
├── reports/                   # Allure results / HTML output
├── Dockerfile
├── requirements.txt
└── pytest.ini