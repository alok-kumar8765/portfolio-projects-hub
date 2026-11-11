
from pathlib import Path
from datetime import datetime
import sqlite3

from database.connection import DATA_DIR

BACKUP_DIR = DATA_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def create_backup():
    source = DATA_DIR / "logitrack.db"

    if not source.exists():
        raise FileNotFoundError("Database not found.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = BACKUP_DIR / f"logitrack_{timestamp}.db"

    with sqlite3.connect(source) as src:
        with sqlite3.connect(destination) as dst:
            src.backup(dst)

    return destination


def list_backups():
    return sorted(
        BACKUP_DIR.glob("logitrack_*.db"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
