#!/usr/bin/env python3
import sys
import os

# Add the Backend directory to the Python path
sys.path.insert(0, r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')

# Change to Backend directory
os.chdir(r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')

from config import Config
from models import db, User
from flask import Flask
from flask_bcrypt import Bcrypt
import sqlite3

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Bcrypt
db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    # Create tables
    db.create_all()
    
    # Check if admin exists
    admin = User.query.filter_by(email='admin@fertilemap.com').first()
    
    if admin:
        print(f"✅ Admin already exists: {admin.email}")
    else:
        # Create admin user
        password_hash = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
        
        new_admin = User(
            email='admin@fertilemap.com',
            password_hash=password_hash,
            full_name='Admin User',
            farm_name='Main Farm',
            role='admin',
            is_active=True
        )
        
        db.session.add(new_admin)
        db.session.commit()
        
        print("=" * 70)
        print("✅ ADMIN USER CREATED SUCCESSFULLY")
        print("=" * 70)
        print(f"\n📧 Email:    admin@fertilemap.com")
        print(f"🔐 Password: Admin@123")
        print(f"👤 Name:     Admin User")
        print(f"🌾 Farm:     Main Farm")
        print(f"👑 Role:     admin")
        print("\n" + "=" * 70)
        print("\n✨ You can now login with these credentials!")
        print("=" * 70)
