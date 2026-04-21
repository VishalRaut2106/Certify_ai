#!/usr/bin/env python3
"""
Test MongoDB connection script
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_mongo_connection():
    """Test MongoDB connection with different configurations"""
    
    mongodb_url = os.getenv("MONGODB_URL")
    print(f"Testing MongoDB connection to: {mongodb_url}")
    
    # Test 1: Basic connection
    try:
        print("\n🔄 Test 1: Basic connection...")
        client = AsyncIOMotorClient(mongodb_url)
        await client.admin.command('ping')
        print("✅ Basic connection successful!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Basic connection failed: {e}")
    
    # Test 2: Connection with SSL parameters
    try:
        print("\n🔄 Test 2: Connection with SSL parameters...")
        client = AsyncIOMotorClient(
            mongodb_url,
            tls=True,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
            serverSelectionTimeoutMS=10000
        )
        await client.admin.command('ping')
        print("✅ SSL connection successful!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ SSL connection failed: {e}")
    
    # Test 3: Connection without SSL
    try:
        print("\n🔄 Test 3: Connection without SSL...")
        # Remove SSL parameters from URL
        url_without_ssl = mongodb_url.replace("&tls=true&tlsAllowInvalidCertificates=true", "")
        client = AsyncIOMotorClient(
            url_without_ssl,
            serverSelectionTimeoutMS=10000
        )
        await client.admin.command('ping')
        print("✅ Non-SSL connection successful!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Non-SSL connection failed: {e}")
    
    print("\n❌ All connection attempts failed!")
    return False

if __name__ == "__main__":
    asyncio.run(test_mongo_connection())