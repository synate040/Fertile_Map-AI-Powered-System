#!/usr/bin/env python3
"""Test analyze endpoint"""
import requests
import json
from PIL import Image
import io

# Create a test image
img = Image.new('RGB', (224, 224), color=(139, 90, 43))
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Get token (you'll need to set this)
login_url = 'http://localhost:5000/api/login'
analyze_url = 'http://localhost:5000/api/analyze'

# Login first
print("1. Logging in...")
login_response = requests.post(login_url, json={
    'email': 'admin@fertilemap.com',
    'password': 'Admin@123'
})

if login_response.status_code != 200:
    print(f"Login failed: {login_response.text}")
    exit(1)

token = login_response.json()['data']['token']
print(f"✅ Login successful, token: {token[:20]}...")

# Upload and analyze
print("\n2. Uploading image and analyzing...")
headers = {'Authorization': f'Bearer {token}'}

files = {
    'image': ('test.png', img_bytes, 'image/png')
}
data = {
    'crop_type': 'maize'
}

response = requests.post(analyze_url, headers=headers, files=files, data=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    print("\n✅ Analysis successful!")
else:
    print(f"\n❌ Analysis failed: {response.json()}")
