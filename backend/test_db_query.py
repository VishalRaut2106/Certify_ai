#!/usr/bin/env python3
"""
Test database query for user lookup
"""

import asyncio
from app.core.database import get_database

async def test_user_lookup():
    """Test user lookup in database"""
    
    db = get_database()
    
    # Test user lookup
    email = "test@example.com"
    print(f"Looking up user with email: {email}")
    
    user_doc = await db.users.find_one({"email": email})
    
    if user_doc:
        print("✅ User found!")
        print(f"User ID: {user_doc['id']}")
        print(f"Email: {user_doc['email']}")
        print(f"Full name: {user_doc['full_name']}")
        print(f"Hashed password: {user_doc['hashed_password'][:20]}...")
    else:
        print("❌ User not found!")
        
        # List all users
        print("\nAll users in database:")
        all_users = await db.users.find()
        for user in all_users:
            print(f"  - {user['email']} (ID: {user['id']})")

if __name__ == "__main__":
    asyncio.run(test_user_lookup())