#!/usr/bin/env python3
"""Simple debug script for analysis"""
import sys
import os

sys.path.insert(0, r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')
os.chdir(r'C:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\Backend')

from PIL import Image
import numpy as np

print("Testing predict method...")

try:
    from services.soil_analyzer import analyzer
    
    # Create test image
    img = Image.new('RGB', (224, 224), color=(139, 90, 43))
    test_path = 'test.jpg'
    img.save(test_path)
    
    # Run predict
    result = analyzer.predict(test_path)
    
    print("SUCCESS - Result keys:", list(result.keys()))
    print("Soil type:", result.get('soil_type'))
    print("Confidence:", result.get('confidence'))
    print("Properties:", result.get('properties'))
    print("All predictions:", result.get('all_predictions'))
    
    os.remove(test_path)
    
except Exception as e:
    import traceback
    print("ERROR:")
    traceback.print_exc()
