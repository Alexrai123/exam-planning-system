EXAM PLANNING SYSTEM - SETUP AND RUNNING INSTRUCTIONS
==================================================

INITIAL SETUP
-------------
1. Create a virtual environment:
   python -m venv venv

2. Activate the virtual environment:
   .\venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Initialize the database (only needed once):
   cd backend
   python init_db.py


RUNNING THE APPLICATION
----------------------
1. Activate the virtual environment (if not already activated):
   .\venv\Scripts\activate

2. Start the FastAPI application:
   cd backend
   python run.py

3. Access the application:
   - API documentation: http://localhost:8000/docs
   - API endpoints: http://localhost:8000/api/v1/...


SAMPLE USERS
-----------
The system is initialized with the following sample users:

1. Admin (Secretariat role):
   - Email: admin@example.com
   - Password: password

2. Professor:
   - Email: professor@example.com
   - Password: password

3. Student:
   - Email: student@example.com
   - Password: password


API ENDPOINTS
------------
- Authentication: /api/v1/auth/login, /api/v1/auth/register
- Users: /api/v1/users
- Courses: /api/v1/courses
- Groups: /api/v1/groups
- Rooms: /api/v1/rooms
- Exams: /api/v1/exams
- Exports: /api/v1/exports


SWAGGER AUTHORIZATION
-------------------
To authorize in Swagger UI:

1. Get your access token:
   - Go to http://localhost:8000/docs
   - Find and expand the /api/v1/auth/login endpoint
   - Click "Try it out"
   - For username, enter your email (e.g., admin@example.com)
   - For password, enter your password (e.g., password)
   - Click "Execute"
   - Copy the access_token from the response

2. Use the token to authorize:
   - Click the "Authorize" button at the top right
   - Enter your token as: Bearer your_token_here
   - Click "Authorize" then "Close"


RESETTING THE DATABASE
--------------------
To reset the database to its initial state:
1. Delete the test.db file in the backend directory
2. Run the initialization script again:
   cd backend
   python init_db.py


STOPPING THE APPLICATION
----------------------
To stop the application, press Ctrl+C in the terminal where it's running.
