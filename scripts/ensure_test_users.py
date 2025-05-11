import sys
import os
import psycopg2
from psycopg2.extras import DictCursor
from passlib.context import CryptContext

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database connection parameters
db_params = {
    "dbname": "exam_planning",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

# Test users to ensure exist in the database
test_users = [
    {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "password123",
        "role": "SECRETARIAT"
    },
    {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "password": "password123",
        "role": "PROFESSOR"
    },
    {
        "name": "Emma Wilson",
        "email": "emma.wilson@example.com",
        "password": "password123",
        "role": "STUDENT"
    }
]

def ensure_test_users():
    """Ensure test users exist in the database with correct credentials"""
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        for user in test_users:
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (user["email"],))
            existing_user = cursor.fetchone()
            
            hashed_password = pwd_context.hash(user["password"])
            
            if existing_user:
                # Update existing user
                cursor.execute(
                    "UPDATE users SET name = %s, password = %s, role = %s WHERE email = %s",
                    (user["name"], hashed_password, user["role"], user["email"])
                )
                print(f"Updated user: {user['email']}")
            else:
                # Create new user
                cursor.execute(
                    "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (user["name"], user["email"], hashed_password, user["role"])
                )
                print(f"Created user: {user['email']}")
        
        # Commit the changes
        conn.commit()
        
        # Print all users for verification
        cursor.execute("SELECT id, name, email, role FROM users")
        all_users = cursor.fetchall()
        
        print("\nAll users in the database:")
        for user in all_users:
            print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Role: {user['role']}")
        
        print("\nTest credentials:")
        for user in test_users:
            print(f"Email: {user['email']}, Password: {user['password']}, Role: {user['role']}")
        
        # Close the connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error ensuring test users: {e}")

if __name__ == "__main__":
    ensure_test_users()
