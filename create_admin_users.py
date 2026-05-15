#!/usr/bin/env python3
"""Create multiple admin users in the database"""
import sys
sys.path.insert(0, r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')

from config import Config
from models import db, User
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)

# Admin users to create
admin_users = [
    {
        'email': 'admin1@fertilemap.com',
        'password': 'Admin@123',
        'full_name': 'Sarah Admin',
        'farm_name': 'North Farm Admin'
    },
    {
        'email': 'admin2@fertilemap.com',
        'password': 'Admin@123',
        'full_name': 'John Developer',
        'farm_name': 'Development Farm'
    },
    {
        'email': 'admin3@fertilemap.com',
        'password': 'Admin@123',
        'full_name': 'Maria Support',
        'farm_name': 'Support Center'
    },
]

with app.app_context():
    print("🚀 Creating additional admin users...\n")
    
    created_count = 0
    existing_count = 0
    
    for admin_data in admin_users:
        try:
            # Check if user already exists
            existing = User.query.filter_by(email=admin_data['email']).first()
            
            if existing:
                print(f"⚠️  Already exists: {admin_data['email']}")
                existing_count += 1
                continue
            
            # Create new admin user
            password_hash = bcrypt.generate_password_hash(admin_data['password']).decode('utf-8')
            
            new_admin = User(
                email=admin_data['email'],
                password_hash=password_hash,
                full_name=admin_data['full_name'],
                farm_name=admin_data['farm_name'],
                role='admin',
                is_active=True
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            print(f"✅ Created: {admin_data['email']}")
            print(f"   Name: {admin_data['full_name']}")
            print(f"   Farm: {admin_data['farm_name']}\n")
            
            created_count += 1
            
        except Exception as e:
            print(f"❌ Error creating {admin_data['email']}: {e}\n")
            db.session.rollback()
    
    # Show summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Created: {created_count} new admin users")
    print(f"⚠️  Already existed: {existing_count} users")
    
    # List all admins
    all_admins = User.query.filter_by(role='admin').all()
    print(f"\n👥 Total admin users: {len(all_admins)}")
    print("\nAll Admin Users:")
    for i, admin in enumerate(all_admins, 1):
        print(f"  {i}. {admin.email} - {admin.full_name}")
    
    print("\n" + "=" * 70)
    print("✨ Admin user creation complete!")
    print("=" * 70)
