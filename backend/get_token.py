import requests
import json

def get_token(email, password):
    """Get an authentication token for the API"""
    url = "http://localhost:8000/api/v1/auth/login"
    data = {
        "username": email,  # OAuth2 form uses 'username' field for email
        "password": password
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
    print("=== Exam Planning System - Get Authentication Token ===")
    print("\nSample users:")
    print("1. Admin (Secretariat): admin@example.com / password")
    print("2. Professor: professor@example.com / password")
    print("3. Student: student@example.com / password")
    
    email = input("\nEnter email: ")
    password = input("Enter password: ")
    
    get_token(email, password)
