import requests
import json

def get_token():
    """Get an authentication token for the admin user"""
    url = "http://localhost:8000/api/v1/auth/login"
    data = {
        "username": "admin@example.com",  # OAuth2 form uses 'username' field for email
        "password": "password"
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            print("\n=== Authentication Successful ===")
            print(f"Access Token: {token_data['access_token']}")
            print("\nTo use this token in Swagger UI:")
            print("1. Click the 'Authorize' button at the top right")
            print("2. Enter the following in the value field:")
            print(f"   Bearer {token_data['access_token']}")
            print("3. Click 'Authorize' and then 'Close'")
            return token_data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None

if __name__ == "__main__":
    print("=== Getting Admin Token ===")
    get_token()
