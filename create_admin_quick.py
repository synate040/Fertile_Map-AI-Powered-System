#!/usr/bin/env python
"""Quick script to create admin user"""
import sqlite3
import hashlib
import bcrypt
import os

# Database path
db_path = r"C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend\database\soil_app.db"

# Admin credentials
admin_email = "admin@fertilemap.com"
admin_password = "Admin@123"
admin_name = "Admin User"
admin_farm = "Main Farm"

# Hash password using bcrypt
password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
    existing = cursor.fetchone()
    
    if existing:
        print(f"❌ Admin user already exists with email: {admin_email}")
        conn.close()
        exit(1)
    
    # Create admin user
    cursor.execute('''
        INSERT INTO users (email, password_hash, full_name, farm_name, role, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''', (admin_email, password_hash, admin_name, admin_farm, 'admin', 1))
    
    conn.commit()
    
    print("=" * 70)
    print("✅ ADMIN USER CREATED SUCCESSFULLY")
    print("=" * 70)
    print(f"\n📧 Email:    {admin_email}")
    print(f"🔐 Password: {admin_password}")
    print(f"👤 Name:     {admin_name}")
    print(f"🌾 Farm:     {admin_farm}")
    print(f"👑 Role:     admin")
    print("\n" + "=" * 70)
    print("\n✨ You can now login to the admin panel with these credentials:")
    print("=" * 70)
    
    conn.close()
    print("\n✅ Done!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
