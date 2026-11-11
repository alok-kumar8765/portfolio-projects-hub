
from database.connection import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)

print("\n========== DATABASE TABLES ==========")

tables = inspector.get_table_names()

for table in tables:
    print(f"\nTABLE: {table}")
    for column in inspector.get_columns(table):
        print(
            f"  {column['name']} "
            f"({column['type']})"
        )

print("\n========== ALEMBIC VERSION ==========")

if "alembic_version" in tables:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT version_num FROM alembic_version")
        )
        for row in result:
            print("Current version:", row[0])
else:
    print("Alembic version table does not exist.")
