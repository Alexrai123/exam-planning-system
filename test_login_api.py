"""
Test script to verify login functionality and token handling
"""
import requests
import json

API_URL = 'http://localhost:8000/api/v1'
EMAIL = 'ana.petrescu@student.usv.ro'
PASSWORD = 'Student2025!'

def test_login():
    """Test login and token handling"""
    print(f"Attempting to login with {EMAIL}")
    
    # Login request
    login_data = {
        'username': EMAIL,
        'password': PASSWORD
    }
    
    try:
        login_response = requests.post(
            f"{API_URL}/auth/login", 
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        print(f"Login status code: {login_response.status_code}")
        
        if login_response.status_code == 200:
            response_data = login_response.json()
            print("Login response:", json.dumps(response_data, indent=2))
            
            if 'access_token' in response_data:
                token = response_data['access_token']
                print(f"Token received: {token[:20]}...")
                
                # Save token to file
                with open('token.txt', 'w') as f:
                    f.write(token)
                
                # Test token by making a request to get user info
                try:
                    user_response = requests.get(
                        f"{API_URL}/users/me",
                        headers={'Authorization': f"Bearer {token}"}
                    )
                    
                    print(f"User info status code: {user_response.status_code}")
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        print("User info:", json.dumps(user_data, indent=2))
                    else:
                        print("Failed to get user info:", user_response.text)
                        
                    # Test another endpoint
                    exams_response = requests.get(
                        f"{API_URL}/exams/",
                        headers={'Authorization': f"Bearer {token}"}
                    )
                    
                    print(f"Exams status code: {exams_response.status_code}")
                    
                    if exams_response.status_code == 200:
                        exams_data = exams_response.json()
                        print(f"Retrieved {len(exams_data)} exams")
                    else:
                        print("Failed to get exams:", exams_response.text)
                        
                except Exception as e:
                    print(f"Error testing token: {str(e)}")
            else:
                print("No token in response")
        else:
            print("Login failed:", login_response.text)
    
    except Exception as e:
        print(f"Error during login: {str(e)}")

if __name__ == "__main__":
    test_login()
