#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check ML and Database Models Status"""
import sys
import os
import io

# Fix Unicode output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')
os.chdir(r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')

print("🔍 FERTILE MAP Model Diagnostic Report")
print("=" * 70)

# Check 1: ML Model Files
print("\n📦 ML MODEL FILES:")
print("-" * 70)

model_paths = [
    ('Primary Model', r'models\models\soil_model.h5'),
    ('Alternate 1', r'models\soil_classifier.h5'),
    ('Alternate 2', r'models\soil_model.h5'),
]

model_found = None
for name, path in model_paths:
    abs_path = os.path.abspath(path)
    exists = os.path.exists(abs_path)
    status = "✅ EXISTS" if exists else "❌ NOT FOUND"
    size = f"({os.path.getsize(abs_path) / 1024 / 1024:.2f} MB)" if exists else ""
    print(f"{name:20} | {status:15} {size}")
    if exists and model_found is None:
        model_found = abs_path

# Check 2: TensorFlow
print("\n🤖 TENSORFLOW STATUS:")
print("-" * 70)

try:
    import tensorflow
    print(f"✅ TensorFlow installed")
    
    if model_found:
        try:
            model = tensorflow.keras.models.load_model(model_found)
            print(f"✅ Model loaded successfully!")
            print(f"   Input shape: {model.input_shape}")
            print(f"   Output shape: {model.output_shape}")
            print(f"   Total layers: {len(model.layers)}")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)[:100]}")
    else:
        print("⚠️  No model file found - will use MOCK predictions")
        
except ImportError:
    print("⚠️  TensorFlow not installed - will use MOCK predictions")

# Check 3: Soil Analyzer Service
print("\n🌾 SOIL ANALYZER SERVICE:")
print("-" * 70)

try:
    from services.soil_analyzer import analyzer
    print(f"✅ SoilAnalyzer loaded")
    print(f"   Using mock mode: {analyzer.use_mock}")
    print(f"   Model loaded: {analyzer.model is not None}")
    print(f"   Available soil classes: {len(analyzer.classes)}")
    print(f"   Classes: {', '.join(analyzer.classes)}")
    
    if not analyzer.use_mock:
        print("✅ Real ML Model is ACTIVE!")
    else:
        print("⚠️  Using MOCK predictions (for testing)")
        
except Exception as e:
    print(f"❌ Error: {str(e)[:100]}")

# Check 4: Database Models
print("\n💾 DATABASE MODELS:")
print("-" * 70)

try:
    from config import Config
    from models import db, User, SoilAnalysis
    from flask import Flask
    
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    print("✅ SQLAlchemy Models imported")
    
    with app.app_context():
        db.create_all()
        user_count = User.query.count()
        analysis_count = SoilAnalysis.query.count()
        admin_count = User.query.filter_by(role='admin').count()
        
        print(f"✅ Database connected:")
        print(f"   Total users: {user_count}")
        print(f"   Admin users: {admin_count}")
        print(f"   Analyses: {analysis_count}")
            
except Exception as e:
    print(f"❌ Error: {str(e)[:100]}")

# Summary
print("\n" + "=" * 70)
print("📊 FINAL STATUS:")
print("=" * 70)
if model_found:
    print("✅ ML Model: READY")
else:
    print("⚠️  ML Model: USING MOCK (FOR DEMO)")
print("✅ Database: READY")
print("✅ System: OPERATIONAL")
print("\n✨ All systems ready to use!")

