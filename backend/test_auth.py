#!/usr/bin/env python3
"""
Test authentication endpoints
"""

import asyncio
import aiohttp
import json

async def test_auth_endpoints():
    """Test authentication endpoints"""
    
    base_url = "http://127.0.0.1:8000/api/v1"
    
    async with aiohttp.ClientSession() as session:
        # Test register
        print("🔄 Testing register endpoint...")
        register_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User",
            "role": "teacher"
        }
        
        try:
            async with session.post(
                f"{base_url}/auth/register",
                json=register_data,
                headers={"Origin": "http://localhost:3000"}
            ) as response:
                print(f"Register Status: {response.status}")
                print(f"Register Headers: {dict(response.headers)}")
                text = await response.text()
                print(f"Register Response: {text}")
                
        except Exception as e:
            print(f"Register Error: {e}")
        
        # Test login
        print("\n🔄 Testing login endpoint...")
        login_data = aiohttp.FormData()
        login_data.add_field('username', 'test@example.com')
        login_data.add_field('password', 'testpass123')
        
        try:
            async with session.post(
                f"{base_url}/auth/login",
                data=login_data,
                headers={"Origin": "http://localhost:3000"}
            ) as response:
                print(f"Login Status: {response.status}")
                print(f"Login Headers: {dict(response.headers)}")
                text = await response.text()
                print(f"Login Response: {text}")
                
        except Exception as e:
            print(f"Login Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_auth_endpoints())