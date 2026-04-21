#!/usr/bin/env python3
"""
Debug user data in database
"""

import asyncio
import sqlite3
import hashlib

async def debug_user():
    """Check user data in SQLite database"""
    
    # Connect to SQLite database
    conn = sqlite3.connect("certificate_verification.db")
    cursor = conn.cursor()
    
    # Get user data
    cursor.execute("SELECT * FROM users WHERE email = ?", ("test@example.com",))
    user = cursor.fetchone()
    
    if user:
        print("User found:")
        columns = [description[0] for description in cursor.description]
        user_dict = dict(zip(columns, user))
        for key, value in user_dict.items():
            print(f"  {key}: {value}")
        
        # Test password hashing
        test_password = "testpass123"
        stored_hash = user_dict["hashed_password"]
        
        print(f"\nPassword verification test:")
        print(f"  Test password: {test_password}")
        print(f"  Stored hash: {stored_hash}")
        
        # Test SHA256 hash
        sha256_hash = hashlib.sha256(test_password.encode()).hexdigest()
        print(f"  SHA256 of test password: {sha256_hash}")
        print(f"  Hashes match: {sha256_hash == stored_hash}")
        
    else:
        print("User not found")
    
    conn.close()

if __name__ == "__main__":
    asyncio.run(debug_user())