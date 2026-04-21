#!/usr/bin/env python3
"""
Simple test to create a fresh user and test login
"""

import requests
import json
import uuid

def test_fresh_user():
    """Create a fresh user and test login"""
    
    # Generate unique email
    unique_id = str(uuid.uuid4())[:8]
    email = f"testuser_{unique_id}@example.com"
    password = "testpass123"
    
    print(f"Creating user with email: {email}")
    
    # 1. Register new user
    user_data = {
        "email": email,
        "password": password,
        "full_name": "Test User",
        "role": "student",
        "institution_name": "Test University"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/register", json=user_data)
        print(f"Registration response: {response.status_code}")
        if response.status_code in [200, 201]:
            print("✅ User registration successful")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None
    
    # 2. Login with new user
    login_data = {
        "username": email,
        "password": password
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/login", data=login_data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful")
            print(f"Token: {token_data.get('access_token')[:50]}...")
            return token_data.get('access_token')
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

if __name__ == "__main__":
    test_fresh_user()