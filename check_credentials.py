#!/usr/bin/env python3
"""Check database and reset credentials if needed"""
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

with app.app_context():
    try:
        # Check admin user
        admin = User.query.filter_by(email='admin@fertilemap.com').first()
        
        if admin:
            print(f"✅ Admin user found:")
            print(f"   Email: {admin.email}")
            print(f"   Name: {admin.full_name}")
            print(f"   Role: {admin.role}")
            print(f"   Active: {admin.is_active}")
            
            # Reset password to ensure it works
            print("\n🔄 Resetting admin password...")
            new_hash = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
            admin.password_hash = new_hash
            db.session.commit()
            
            print("\n" + "=" * 70)
            print("✅ ADMIN CREDENTIALS RESET")
            print("=" * 70)
            print(f"\n📧 Email:    admin@fertilemap.com")
            print(f"🔐 Password: Admin@123")
            print("\n" + "=" * 70)
        else:
            print("❌ Admin user not found. Creating new admin...")
            
            pw_hash = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
            admin_user = User(
                email='admin@fertilemap.com',
                password_hash=pw_hash,
                full_name='Admin User',
                farm_name='Main Farm',
                role='admin',
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            
            print("\n" + "=" * 70)
            print("✅ ADMIN USER CREATED")
            print("=" * 70)
            print(f"\n📧 Email:    admin@fertilemap.com")
            print(f"🔐 Password: Admin@123")
            print("\n" + "=" * 70)
        
        # List all users
        all_users = User.query.all()
        print(f"\n📊 Total users in database: {len(all_users)}")
        for user in all_users:
            print(f"   - {user.email} ({user.role})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
