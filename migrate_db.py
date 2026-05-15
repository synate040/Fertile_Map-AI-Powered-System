import sqlite3
import os
import shutil
from config import Config

# Backup existing database
db_path = Config.DATABASE
backup_path = db_path + '.backup'

if os.path.exists(db_path):
    shutil.copy(db_path, backup_path)
    print(f"✓ Database backed up to: {backup_path}")
    
    # Delete old database to recreate with new schema
    os.remove(db_path)
    print(f"✓ Old database removed")

# Initialize new database with updated schema
from db import init_db
init_db()
print("✓ Database initialized with new schema (includes role column)")

# Verify the schema
db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
db.close()

print("\nUsers table structure:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")
