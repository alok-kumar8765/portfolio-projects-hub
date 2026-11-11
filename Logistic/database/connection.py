
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATA_DIR / "logitrack.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"


# =========================================================
# SQLALCHEMY ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    },
    echo=False,
    pool_pre_ping=True,
)


# =========================================================
# SQLITE FOREIGN KEY SUPPORT
# =========================================================

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# =========================================================
# DATABASE SESSION
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# =========================================================
# DECLARATIVE BASE
# =========================================================

class Base(DeclarativeBase):
    pass


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def initialize_database():
    from database import models

    Base.metadata.create_all(bind=engine)
#def initialize_database():
#    """Database schema is managed by Alembic migrations."""
#    pass

# =========================================================
# SESSION HELPER
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
