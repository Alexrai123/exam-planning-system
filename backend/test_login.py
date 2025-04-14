import requests
import json

def test_login():
    """Test login with admin credentials"""
    url = "http://localhost:8000/api/v1/auth/login"
    data = {
        "username": "admin@example.com",
        "password": "password"
    }
    
    try:
        # First, try with JSON format
        print("Trying login with JSON format...")
        response = requests.post(url, json=data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # If that fails, try with form data
        print("\nTrying login with form data...")
        response = requests.post(url, data=data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
