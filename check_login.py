#!/usr/bin/env python3
"""
Login Helper - Check existing users and test login
"""

import sqlite3
import requests
import getpass

def show_existing_users():
    """Show all users in the database"""
    try:
        conn = sqlite3.connect('backend/certificate_verification.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT email, full_name, role, created_at FROM users ORDER BY created_at DESC')
        results = cursor.fetchall()
        
        print("\n📋 Existing Users in Database:")
        print("=" * 60)
        
        if results:
            for i, (email, full_name, role, created_at) in enumerate(results, 1):
                print(f"{i}. 📧 Email: {email}")
                print(f"   👤 Name: {full_name}")
                print(f"   🎭 Role: {role}")
                print(f"   📅 Created: {created_at}")
                print("-" * 40)
        else:
            print("❌ No users found in database")
        
        conn.close()
        return results
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        return []

def test_login(email, password):
    """Test login with given credentials"""
    try:
        login_data = {
            "username": email,
            "password": password
        }
        
        print(f"\n🔐 Testing login for: {email}")
        
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/login", data=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful!")
            print(f"🔑 Token: {token_data.get('access_token')[:30]}...")
            print(f"👤 User: {token_data.get('user', {}).get('full_name', 'Unknown')}")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"📝 Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def create_new_user():
    """Create a new user account"""
    print("\n🆕 Create New User Account")
    print("=" * 40)
    
    email = input("📧 Enter email: ").strip()
    password = getpass.getpass("🔒 Enter password: ")
    full_name = input("👤 Enter full name: ").strip()
    
    print("\n🎭 Select role:")
    print("1. Student")
    print("2. Teacher") 
    print("3. Evaluator")
    print("4. Admin")
    
    role_choice = input("Enter choice (1-4): ").strip()
    role_map = {"1": "student", "2": "teacher", "3": "evaluator", "4": "admin"}
    role = role_map.get(role_choice, "student")
    
    institution = input("🏫 Enter institution name: ").strip()
    
    user_data = {
        "email": email,
        "password": password,
        "full_name": full_name,
        "role": role,
        "institution_name": institution
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/register", json=user_data)
        
        if response.status_code in [200, 201]:
            print("✅ User created successfully!")
            print(f"📧 Email: {email}")
            print(f"🎭 Role: {role}")
            
            # Test login immediately
            return test_login(email, password)
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"📝 Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def main():
    """Main function"""
    print("🔐 Certificate Verification System - Login Helper")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code != 200:
            print("❌ Backend server is not running!")
            print("Please start the backend server first:")
            print("cd certificate-verification-system/backend")
            print("uvicorn main:app --reload --host 127.0.0.1 --port 8000")
            return
    except:
        print("❌ Cannot connect to backend server!")
        print("Please start the backend server first.")
        return
    
    # Show existing users
    users = show_existing_users()
    
    if not users:
        print("\n🆕 No users found. Let's create your first account!")
        create_new_user()
        return
    
    print("\n🔐 Login Options:")
    print("1. Login with existing account")
    print("2. Create new account")
    print("3. Reset/recreate account")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Login with existing account
        print("\n📧 Available emails:")
        for i, (email, name, role, _) in enumerate(users, 1):
            print(f"{i}. {email} ({name} - {role})")
        
        email_choice = input("\nEnter email number or type email directly: ").strip()
        
        if email_choice.isdigit() and 1 <= int(email_choice) <= len(users):
            email = users[int(email_choice) - 1][0]
        else:
            email = email_choice
        
        password = getpass.getpass("🔒 Enter password: ")
        test_login(email, password)
        
    elif choice == "2":
        # Create new account
        create_new_user()
        
    elif choice == "3":
        # Reset account
        email = input("📧 Enter email to reset: ").strip()
        password = getpass.getpass("🔒 Enter new password: ")
        
        # Delete existing user if exists
        try:
            conn = sqlite3.connect('backend/certificate_verification.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE email = ?', (email,))
            conn.commit()
            conn.close()
            print(f"🗑️ Deleted existing account for {email}")
        except:
            pass
        
        # Create new account
        full_name = input("👤 Enter full name: ").strip()
        role = input("🎭 Enter role (student/teacher/evaluator/admin): ").strip() or "student"
        institution = input("🏫 Enter institution: ").strip()
        
        user_data = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "role": role,
            "institution_name": institution
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/api/v1/auth/register", json=user_data)
            if response.status_code in [200, 201]:
                print("✅ Account recreated successfully!")
                test_login(email, password)
            else:
                print(f"❌ Failed to recreate account: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()