#!/usr/bin/env python3
"""
Simple test for auth endpoint
"""

import requests
import json

def test_register():
    """Test register endpoint"""
    url = "http://127.0.0.1:8000/api/v1/auth/register"
    data = {
        "email": "frontend@test.com",
        "password": "testpass123",
        "full_name": "Frontend User",
        "role": "teacher"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Origin": "http://localhost:3000"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Testing register endpoint...")
    success = test_register()
    print(f"✅ Success: {success}" if success else "❌ Failed")