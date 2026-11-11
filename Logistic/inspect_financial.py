
from database.connection import engine
from sqlalchemy import text

with engine.connect() as conn:

    for table in ["invoices", "expenses"]:

        print(f"\n========== {table.upper()} ==========")

        count = conn.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar()

        print("Existing records:", count)

        rows = conn.execute(
            text(f"SELECT * FROM {table} LIMIT 5")
        ).fetchall()

        for row in rows:
            print(dict(row._mapping))
