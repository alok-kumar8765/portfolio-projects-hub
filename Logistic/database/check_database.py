
from database.connection import engine
from sqlalchemy import inspect

print("APPLICATION DATABASE:")
print(engine.url)

print("\nDATABASE FILE:")
print(engine.url.database)

print("\nEXISTING TABLES:")
for table in inspect(engine).get_table_names():
    print(table)
