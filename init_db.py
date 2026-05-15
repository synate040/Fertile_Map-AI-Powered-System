#!/usr/bin/env python3
"""Initialize database and create admin user"""
import sys
import os

# Add paths
sys.path.insert(0, r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')
os.chdir(r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')

from config import Config
from models import db, User, SoilAnalysis
from flask import Flask
from flask_bcrypt import Bcrypt
from datetime import datetime

print("🚀 Initializing FERTILE MAP Database...")

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    try:
        # Create all tables based on models
        print("📝 Creating database tables...")
        db.create_all()
        print("✅ Database tables created")
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@fertilemap.com').first()
        
        if admin:
            print(f"⚠️  Admin user already exists: {admin.email}")
        else:
            print("👤 Creating admin user...")
            # Create admin user
            password_hash = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
            
            admin_user = User(
                email='admin@fertilemap.com',
                password_hash=password_hash,
                full_name='Admin User',
                farm_name='Main Farm',
                role='admin',
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("=" * 70)
            print("✅ ADMIN USER CREATED SUCCESSFULLY")
            print("=" * 70)
            print(f"\n📧 Email:    admin@fertilemap.com")
            print(f"🔐 Password: Admin@123")
            print(f"👤 Full Name: Admin User")
            print(f"🌾 Farm Name: Main Farm")
            print(f"👑 Role:      admin")
            print("\n" + "=" * 70)
            print("\n✨ You can now login with these credentials!")
            print("=" * 70)
        
        # Show database stats
        user_count = User.query.count()
        print(f"\n📊 Database Stats:")
        print(f"   Total Users: {user_count}")
        
        print("\n✅ Initialization complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
