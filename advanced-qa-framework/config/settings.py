import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Literal

# Determine environment from OS environment variable (defaults to dev)
current_env = os.getenv("ENV", "dev")
env_file_path = os.path.join("config", "environments", f"{current_env}.env")

class Settings(BaseSettings):
    ENV: Literal["dev", "staging", "prod"] = "dev"
    BASE_URL: str = "https://the-internet.herokuapp.com"
    BROWSER: Literal["chromium", "firefox", "webkit"] = "chromium"
    HEADLESS: bool = True
    TIMEOUT: int = 30000
    RETRY_COUNT: int = 2
    
    # Cloud Grid Configurations
    USE_CLOUD_GRID: bool = False
    CLOUD_PROVIDER: str = "browserstack"  # options: browserstack, saucelabs
    CLOUD_USERNAME: str = ""
    CLOUD_ACCESS_KEY: str = ""

    # Add these lines inside your Settings class in config/settings.py
    TESTRAIL_URL: str = ""
    TESTRAIL_USER: str = ""
    TESTRAIL_APIKEY: str = ""
    TESTRAIL_RUN_ID: str = "1"

    model_config = ConfigDict(
        env_file=env_file_path if os.path.exists(env_file_path) else ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()