# ==================== DATABASE MODELS ====================
"""
SQLAlchemy ORM Models for FERTILE MAP
Replaces raw SQL with modern ORM pattern
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    farm_name = db.Column(db.String(255))
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('SoilAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'farm_name': self.farm_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class SoilAnalysis(db.Model):
    """Soil analysis history model"""
    __tablename__ = 'soil_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    image_url = db.Column(db.String(512))
    soil_type = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float)
    properties = db.Column(JSON)
    predictions = db.Column(JSON)
    recommendations = db.Column(JSON)
    selected_crop = db.Column(db.String(100))
    status = db.Column(db.String(50), default='analyzed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert analysis to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_url': self.image_url,
            'soil_type': self.soil_type,
            'confidence': self.confidence,
            'properties': self.properties,
            'predictions': self.predictions,
            'recommendations': self.recommendations,
            'selected_crop': self.selected_crop,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<SoilAnalysis {self.id} - {self.soil_type}>'

class DatabaseInfo(db.Model):
    """Database metadata information"""
    __tablename__ = 'database_info'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert info to dictionary"""
        return {
            'key': self.key,
            'value': self.value,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    def __repr__(self):
        return f'<DatabaseInfo {self.key}>'

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        # Create tables
        db.create_all()
        print("✓ Database tables created successfully")
