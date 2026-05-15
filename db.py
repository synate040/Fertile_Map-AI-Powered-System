import sqlite3
import os
from config import Config

def get_db():
    db = sqlite3.connect(Config.DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    with open(schema_path, 'r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
    print("Database initialized successfully")

if __name__ == '__main__':
    init_db()
