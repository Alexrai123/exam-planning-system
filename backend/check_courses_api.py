import requests
import json

def check_courses_api():
    """Check if the courses API is returning data"""
    print("Checking courses API...")
    
    # Backend URL
    backend_url = "http://localhost:8000/api/v1"
    
    # First get a token by logging in
    try:
        login_data = {
            "username": "test@example.com",
            "password": "test123"
        }
        
        login_response = requests.post(
            f"{backend_url}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code != 200:
            print(f"Login failed with status code: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token_data = login_response.json()
        token = token_data["access_token"]
        print(f"Successfully logged in and got token")
        
        # Now fetch courses with the token
        courses_response = requests.get(
            f"{backend_url}/courses/",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if courses_response.status_code != 200:
            print(f"Failed to fetch courses. Status code: {courses_response.status_code}")
            print(f"Response: {courses_response.text}")
            return
        
        courses = courses_response.json()
        print(f"Successfully fetched {len(courses)} courses")
        
        if len(courses) > 0:
            print("\nFirst 5 courses:")
            for i, course in enumerate(courses[:5]):
                print(f"{i+1}. ID: {course.get('id')}, Name: {course.get('name')}, Professor: {course.get('profesor_name')}")
        else:
            print("No courses returned from the API")
        
    except Exception as e:
        print(f"Error checking courses API: {str(e)}")
    
    print("\nCourses API check completed!")

if __name__ == "__main__":
    check_courses_api()
