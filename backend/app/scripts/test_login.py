import sys
import os
from pathlib import Path
import requests

# Test user credentials
email = "john.doe@student.usv.ro"
password = "password123"

# API URL
API_URL = "http://localhost:8000/api/v1"

def test_login():
    print(f"Testing login with email: {email}")
    
    # Prepare form data for OAuth2 password flow
    form_data = {
        'username': email,
        'password': password
    }
    
    try:
        # Make the login request
        response = requests.post(
            f"{API_URL}/auth/login",
            data=form_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        # Check response
        if response.status_code == 200:
            print("Login successful!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error during login test: {str(e)}")
        return False

if __name__ == "__main__":
    test_login()
