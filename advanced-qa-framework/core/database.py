from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Example configuration using SQLite/Postgres based on settings
DB_URL = getattr(settings, "DATABASE_URL", "sqlite:///./test_automation.db")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:
    @staticmethod
    def seed_test_user(username: str, email: str):
        """Seeds dynamic test user state directly to backend DB."""
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (username, email) VALUES (:username, :email) ON CONFLICT DO NOTHING"),
                {"username": username, "email": email}
            )

    @staticmethod
    def cleanup_test_data(username: str):
        """Teardowns test user data post-execution."""
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM users WHERE username = :username"), {"username": username})