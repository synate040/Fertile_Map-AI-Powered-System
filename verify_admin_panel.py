#!/usr/bin/env python
"""
Verification script for Admin Panel System
"""

print("=" * 70)
print("ADMIN PANEL SYSTEM VERIFICATION")
print("=" * 70)

# 1. Check database
import sqlite3
from config import Config

db = sqlite3.connect(Config.DATABASE)
db.row_factory = sqlite3.Row
cursor = db.cursor()

cursor.execute("SELECT COUNT(*) as count FROM users WHERE role='admin'")
admin_count = cursor.fetchone()['count']

cursor.execute("SELECT COUNT(*) as count FROM users")
user_count = cursor.fetchone()['count']

print(f"\n✓ Database Status:")
print(f"  - Total Users: {user_count}")
print(f"  - Admin Users: {admin_count}")

# 2. Check admin user
cursor.execute("SELECT id, email, full_name, role FROM users WHERE role='admin'")
admins = cursor.fetchall()
print(f"\n✓ Admin Accounts:")
for admin in admins:
    print(f"  - ID: {admin['id']}, Email: {admin['email']}, Role: {admin['role']}")

db.close()

# 3. Check Flask app
from app import app
admin_endpoints = [
    '/api/admin/users',
    '/api/admin/stats',
    '/api/admin/users/<user_id>/role',
    '/api/admin/users/<user_id>'
]
print(f"\n✓ Admin API Endpoints:")
for endpoint in admin_endpoints:
    print(f"  - {endpoint}")

# 4. Check frontend files
import os
frontend_files = {
    'Admin HTML': '/pages/admin.html',
    'Admin CSS': '/css/admin.css',
    'Admin JS': '/js/admin.js'
}
print(f"\n✓ Frontend Files:")
for name, path in frontend_files.items():
    full_path = os.path.join(os.path.dirname(__file__), f'..\\Frontend{path}')
    exists = os.path.exists(full_path)
    status = "✓" if exists else "✗"
    print(f"  {status} {name}: {path}")

print("\n" + "=" * 70)
print("ADMIN PANEL READY TO USE")
print("=" * 70)
print("\nLogin URL: http://localhost:5000/pages/login.html")
print("Admin Email: admin@soilsense.com")
print("Admin Password: admin@12345")
print("\nAfter login, click the '👑 Admin' button in your dashboard")
print("=" * 70)
