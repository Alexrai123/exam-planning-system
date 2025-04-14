import requests
import json

def update_user_passwords():
    base_url = "http://localhost:8000/api/v1"
    
    # First, try to get an admin token
    login_url = f"{base_url}/auth/login"
    login_data = {
        "username": "admin@example.com",
        "password": "password"
    }
    
    try:
        # Login as admin to get token
        login_response = requests.post(
            login_url, 
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code != 200:
            print(f"Admin login failed: {login_response.status_code}")
            print(login_response.text)
            return
        
        token = login_response.json().get("access_token")
        if not token:
            print("No token received from admin login")
            return
        
        print("Admin login successful, got token")
        
        # Get all users to find IDs
        users_url = f"{base_url}/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        users_response = requests.get(users_url, headers=headers)
        if users_response.status_code != 200:
            print(f"Failed to get users: {users_response.status_code}")
            print(users_response.text)
            return
        
        users = users_response.json()
        print(f"Found {len(users)} users")
        
        # Find professor and student users
        professor_id = None
        student_id = None
        professor_data = None
        student_data = None
        
        for user in users:
            if user["email"] == "professor@example.com":
                professor_id = user["id"]
                professor_data = user
                print(f"Found professor user with ID: {professor_id}")
            elif user["email"] == "student@example.com":
                student_id = user["id"]
                student_data = user
                print(f"Found student user with ID: {student_id}")
        
        # Update professor password if found
        if professor_id and professor_data:
            update_url = f"{base_url}/users/{professor_id}"
            # Need to include all required fields for PUT request
            update_data = {
                "name": professor_data["name"],
                "email": professor_data["email"],
                "password": "password",
                "role": professor_data["role"]
            }
            
            update_response = requests.put(
                update_url,
                data=json.dumps(update_data),
                headers=headers
            )
            
            if update_response.status_code == 200:
                print("Professor password updated successfully")
            else:
                print(f"Failed to update professor password: {update_response.status_code}")
                print(update_response.text)
        else:
            print("Professor user not found")
        
        # Update student password if found
        if student_id and student_data:
            update_url = f"{base_url}/users/{student_id}"
            # Need to include all required fields for PUT request
            update_data = {
                "name": student_data["name"],
                "email": student_data["email"],
                "password": "password",
                "role": student_data["role"]
            }
            
            update_response = requests.put(
                update_url,
                data=json.dumps(update_data),
                headers=headers
            )
            
            if update_response.status_code == 200:
                print("Student password updated successfully")
            else:
                print(f"Failed to update student password: {update_response.status_code}")
                print(update_response.text)
        else:
            print("Student user not found")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    update_user_passwords()
