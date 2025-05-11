import requests
import os
import json

# API base URL
base_url = "http://localhost:8000/api/v1"

# Admin credentials
admin_credentials = {
    "username": "admin@example.com",
    "password": "password123"
}

def test_pdf_export():
    # First, get an access token
    login_url = f"{base_url}/auth/login"
    print(f"Logging in as admin to {login_url}...")
    
    try:
        login_response = requests.post(login_url, data=admin_credentials)
        login_response.raise_for_status()  # Raise exception for non-200 status codes
        
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            print("Failed to get access token. Response:", login_response.text)
            return
        
        print("Successfully obtained access token")
        
        # Now test the PDF export endpoint
        pdf_url = f"{base_url}/exams/export/pdf"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        print(f"Requesting PDF export from {pdf_url}...")
        
        # Make the request with stream=True to handle binary data properly
        pdf_response = requests.get(pdf_url, headers=headers, stream=True)
        pdf_response.raise_for_status()
        
        # Check if we got the correct content type
        content_type = pdf_response.headers.get('Content-Type')
        if 'application/pdf' not in content_type.lower():
            print(f"Warning: Unexpected content type: {content_type}")
        
        # Save the PDF file
        output_path = os.path.join(os.path.dirname(__file__), "exam_schedule_test.pdf")
        with open(output_path, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"PDF file saved to {output_path}")
        print("PDF export test successful!")
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Could not connect to the API. Make sure the backend server is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_pdf_export()
