#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test soil analysis with a sample image"""
import sys
import os
from PIL import Image
import numpy as np

sys.path.insert(0, r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')
os.chdir(r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')

print("=" * 70)
print("Testing Soil Analysis Pipeline")
print("=" * 70)

# Test 1: Load soil analyzer
print("\n1. Loading SoilAnalyzer...")
try:
    from services.soil_analyzer import analyzer
    print("   ✅ SoilAnalyzer loaded")
    print(f"   - Using mock: {analyzer.use_mock}")
    print(f"   - Model loaded: {analyzer.model is not None}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Create a test image
print("\n2. Creating test image...")
try:
    test_image_path = "test_soil.jpg"
    # Create a simple soil-like image (brown/earth tones)
    img = Image.new('RGB', (224, 224), color=(139, 90, 43))  # Brown color
    img.save(test_image_path)
    print(f"   ✅ Test image created: {test_image_path}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Run prediction
print("\n3. Running prediction...")
try:
    result = analyzer.predict(test_image_path)
    print("   ✅ Prediction successful!")
    print(f"   - Soil type: {result['soil_type']}")
    print(f"   - Confidence: {result['confidence']:.2%}")
    print(f"   - All predictions:")
    for soil_type, confidence in result['predictions'].items():
        print(f"     * {soil_type}: {confidence:.2f}%")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Get recommendations
print("\n4. Getting fertilizer recommendations...")
try:
    from services.fertilizer import get_recommendations
    recommendations = get_recommendations(result['soil_type'], 'maize')
    print("   ✅ Recommendations retrieved!")
    print(f"   - Soil type: {result['soil_type']}")
    print(f"   - Crop: maize")
    print(f"   - N: {recommendations.get('nitrogen', 'N/A')}")
    print(f"   - P: {recommendations.get('phosphorus', 'N/A')}")
    print(f"   - K: {recommendations.get('potassium', 'N/A')}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Save to database
print("\n5. Testing database save...")
try:
    from config import Config
    from models import db, User, SoilAnalysis
    from flask import Flask
    
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Get first user
        user = User.query.first()
        if not user:
            print("   ❌ No users in database")
            sys.exit(1)
        
        # Create analysis record
        analysis = SoilAnalysis(
            user_id=user.id,
            image_url='test_soil.jpg',
            soil_type=result['soil_type'],
            confidence=result['confidence'],
            properties=result['properties'],
            predictions=result['predictions'],
            recommendations=recommendations,
            selected_crop='maize',
            status='analyzed'
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        print("   ✅ Analysis saved to database!")
        print(f"   - Analysis ID: {analysis.id}")
        print(f"   - User: {user.email}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

print("\n" + "=" * 70)
print("✅ All tests passed! Analysis pipeline is working correctly.")
print("=" * 70)
