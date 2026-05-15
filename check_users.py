import sqlite3
from config import Config

try:
    db = sqlite3.connect(Config.DATABASE)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    
    # Check users table
    cursor.execute("SELECT id, email, full_name, role FROM users")
    users = cursor.fetchall()
    
    print("=" * 60)
    print("USERS IN DATABASE:")
    print("=" * 60)
    
    if users:
        for user in users:
            role_badge = "👑 ADMIN" if user['role'] == 'admin' else "👤 USER"
            print(f"ID: {user[0]}")
            print(f"Email: {user[1]}")
            print(f"Full Name: {user[2]}")
            print(f"Role: {role_badge}")
            print("-" * 60)
    else:
        print("❌ No users found in database")
        print("\nYou can create an admin account by:")
        print("1. Using the /api/auth/register endpoint")
        print("2. Registering via the frontend at /pages/register.html")
        print("3. Using create_admin.py script")
    
    # Check total count
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()
    print(f"\nTotal Users: {count[0]}")
    
    # Show admin count
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'admin'")
    admin_count = cursor.fetchone()
    print(f"Admin Users: {admin_count[0]}")
    
    db.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
