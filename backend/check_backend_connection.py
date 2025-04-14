import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_backend_connection():
    """Check if the backend API is accessible"""
    print("Checking backend API connection...")
    
    # Backend URL
    backend_url = "http://localhost:8000/api/v1"
    
    try:
        # Try to access the root endpoint
        response = requests.get(f"{backend_url}/")
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        
        # Check CORS headers
        print("\nChecking CORS headers...")
        options_response = requests.options(f"{backend_url}/auth/login")
        print(f"OPTIONS request status: {options_response.status_code}")
        print("Headers:")
        for header, value in options_response.headers.items():
            print(f"  {header}: {value}")
        
        # Check if the login endpoint is accessible
        print("\nChecking login endpoint...")
        try:
            login_response = requests.post(
                f"{backend_url}/auth/login",
                data={"username": "test@example.com", "password": "test123"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            print(f"Login endpoint status: {login_response.status_code}")
            print(f"Response: {login_response.text[:200]}")
        except Exception as e:
            print(f"Error accessing login endpoint: {str(e)}")
        
    except Exception as e:
        print(f"Error connecting to backend: {str(e)}")
    
    print("\nConnection check completed!")

if __name__ == "__main__":
    check_backend_connection()
