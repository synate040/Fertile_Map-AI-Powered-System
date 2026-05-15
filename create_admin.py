#!/usr/bin/env python
"""
Script to create or update an admin user in the database.
Usage: python create_admin.py <email> <password> [full_name] [farm_name]
"""

import sys
import sqlite3
from flask_bcrypt import Bcrypt
from config import Config

def create_admin(email, password, full_name="Admin", farm_name=""):
    """Create an admin user in the database"""
    
    try:
        # Connect to database
        db = sqlite3.connect(Config.DATABASE)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"❌ User with email '{email}' already exists")
            db.close()
            return False
        
        # Hash password
        bcrypt = Bcrypt()
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create admin user
        cursor.execute(
            '''INSERT INTO users (email, password_hash, full_name, farm_name, role, is_active) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (email, password_hash, full_name, farm_name, 'admin', 1)
        )
        db.commit()
        
        # Get the new user
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        db.close()
        
        print("=" * 60)
        print("✅ ADMIN USER CREATED SUCCESSFULLY")
        print("=" * 60)
        print(f"Admin ID: {user['id']}")
        print(f"Email: {email}")
        print(f"Full Name: {full_name}")
        print(f"Role: admin")
        print("=" * 60)
        print("\nYou can now login with these credentials:")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py <email> <password> [full_name] [farm_name]")
        print("\nExample:")
        print("  python create_admin.py admin@example.com mypassword123 'John Doe' 'My Farm'")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3] if len(sys.argv) > 3 else "Admin"
    farm_name = sys.argv[4] if len(sys.argv) > 4 else ""
    
    success = create_admin(email, password, full_name, farm_name)
    sys.exit(0 if success else 1)
