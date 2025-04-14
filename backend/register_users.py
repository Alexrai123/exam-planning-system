import requests
import json

def register_user(name, email, password, role):
    url = "http://localhost:8000/api/v1/auth/register"
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "role": role
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print(f"Successfully registered {role} user: {email}")
            return True
        else:
            print(f"Failed to register {role} user: {email}")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error registering {role} user: {email}")
        print(f"Error: {str(e)}")
        return False

def main():
    # Register professor user
    register_user(
        name="Professor User",
        email="professor@example.com",
        password="password",
        role="PROFESSOR"
    )
    
    # Register student user
    register_user(
        name="Student User",
        email="student@example.com",
        password="password",
        role="STUDENT"
    )

if __name__ == "__main__":
    main()
