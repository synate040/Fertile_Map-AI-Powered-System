#!/usr/bin/env python
"""Verify database schema and create/fix admin user"""
import sqlite3
import bcrypt

db_path = r"C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend\database\soil_app.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check table schema
    print("📋 Checking users table schema...")
    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()
    
    print("\nTable Columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Check existing users
    print("\n👥 Existing users:")
    cursor.execute("SELECT id, email, full_name, role FROM users;")
    users = cursor.fetchall()
    
    if users:
        for user in users:
            print(f"  ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}")
    else:
        print("  (No users found)")
    
    # Create admin user
    admin_email = "admin@fertilemap.com"
    admin_password = "Admin@123"
    admin_name = "Admin User"
    admin_farm = "Main Farm"
    
    # Check if admin already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
    existing = cursor.fetchone()
    
    if existing:
        print(f"\n⚠️  Admin already exists with ID: {existing[0]}")
    else:
        # Hash password
        password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        
        # Try inserting with password_hash column
        try:
            cursor.execute('''
                INSERT INTO users (email, password_hash, full_name, farm_name, role, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (admin_email, password_hash, admin_name, admin_farm, 'admin', 1))
            
            conn.commit()
            print("\n✅ Admin user created successfully!")
            print(f"📧 Email:    {admin_email}")
            print(f"🔐 Password: {admin_password}")
        except Exception as e:
            print(f"\n❌ Error with password_hash column: {e}")
            print("Trying with 'password' column instead...")
            
            try:
                cursor.execute('''
                    INSERT INTO users (email, password, full_name, farm_name, role, is_active, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ''', (admin_email, password_hash, admin_name, admin_farm, 'admin', 1))
                
                conn.commit()
                print("\n✅ Admin user created successfully (using 'password' column)!")
                print(f"📧 Email:    {admin_email}")
                print(f"🔐 Password: {admin_password}")
            except Exception as e2:
                print(f"\n❌ Error with 'password' column: {e2}")
    
    conn.close()
    print("\n✨ Database verification complete!")

except Exception as e:
    print(f"❌ Error: {e}")
