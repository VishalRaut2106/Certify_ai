#!/usr/bin/env python3
import requests

def test_certificates():
    # Login
    url_login = "http://127.0.0.1:8000/api/v1/auth/login"
    data = {"username": "test@example.com", "password": "testpass123"}
    headers = {"Origin": "http://localhost:3000"}
    
    resp_login = requests.post(url_login, data=data, headers=headers)
    if resp_login.status_code != 200:
        print(f"Login failed: {resp_login.text}")
        return
        
    token = resp_login.json().get("access_token")
    print(f"Token: {token}")
    
    # Get certificates
    url_cert = "http://127.0.0.1:8000/api/v1/certificates/?limit=50"
    headers_cert = {
        "Origin": "http://localhost:3000",
        "Authorization": f"Bearer {token}"
    }
    
    resp_cert = requests.get(url_cert, headers=headers_cert)
    print(f"Certificates Status: {resp_cert.status_code}")
    print(f"Response: {resp_cert.text}")

if __name__ == "__main__":
    test_certificates()
