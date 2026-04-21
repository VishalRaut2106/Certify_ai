#!/usr/bin/env python3
"""
Test login endpoint
"""

import requests

def test_login():
    """Test login endpoint"""
    url = "http://127.0.0.1:8000/api/v1/auth/login"
    
    # Form data for OAuth2PasswordRequestForm
    data = {
        "username": "test@example.com",  # OAuth2 uses 'username' field for email
        "password": "testpass123"
    }
    
    headers = {
        "Origin": "http://localhost:3000"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Testing login endpoint...")
    success = test_login()
    print(f"✅ Success: {success}" if success else "❌ Failed")