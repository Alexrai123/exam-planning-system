import requests
import json

# API endpoint
login_url = "http://localhost:8000/api/v1/auth/login"

# Test credentials
credentials = [
    {"username": "secretariat@usv.ro", "password": "password123"},
    {"username": "secretariat@usv.ro", "password": "secretariat123"},
    {"username": "admin@example.com", "password": "password123"},
    {"username": "professor@example.com", "password": "password123"}
]

# Test each set of credentials
for cred in credentials:
    print(f"\nTesting login with: {cred['username']}")
    
    # Format data as form data
    form_data = {
        "username": cred["username"],
        "password": cred["password"]
    }
    
    try:
        # Send POST request
        response = requests.post(login_url, data=form_data)
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Login successful!")
            token = response.json().get("access_token")
            print(f"Token: {token[:20]}...")
            
            # Test getting user info with token
            user_url = "http://localhost:8000/api/v1/users/me"
            headers = {"Authorization": f"Bearer {token}"}
            
            user_response = requests.get(user_url, headers=headers)
            print(f"\nUser Info Status: {user_response.status_code}")
            if user_response.status_code == 200:
                print(f"User Info: {user_response.json()}")
            else:
                print(f"Failed to get user info: {user_response.text}")
        else:
            print("Login failed!")
    
    except Exception as e:
        print(f"Error: {str(e)}")

print("\nLogin testing completed.")
