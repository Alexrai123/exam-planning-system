import psycopg2
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import bcrypt

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("POSTGRES_HOST", "exam_planning_db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "exam_planning")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# Password context for verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    return conn

def get_password_hash(password):
    """Generate a password hash using bcrypt directly"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def create_new_user():
    """Create a new user with a known password"""
    print("Creating a new test user...")
    
    # Test user credentials
    test_email = "test@example.com"
    test_password = "test123"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (test_email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        print(f"User with email {test_email} already exists. Updating password...")
        
        # Update password for existing user
        hashed_password = get_password_hash(test_password)
        cursor.execute("""
            UPDATE users
            SET password = %s
            WHERE email = %s
        """, (hashed_password, test_email))
        
        print(f"Password updated for user {test_email}")
    else:
        # Create a new user
        hashed_password = get_password_hash(test_password)
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, ("Test User", test_email, hashed_password, "SECRETARIAT"))
        
        user_id = cursor.fetchone()[0]
        print(f"Created new test user with ID: {user_id}")
    
    # Print all users with their hashed passwords
    cursor.execute("SELECT id, name, email, password, role FROM users")
    users = cursor.fetchall()
    
    print(f"\nAll users in the database ({len(users)}):")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[4]}")
        print(f"  Password Hash: {user[3][:20]}...")
    
    conn.close()
    
    print("\nUser creation completed!")
    print(f"You can now try to login with:")
    print(f"Email: {test_email}")
    print(f"Password: {test_password}")

if __name__ == "__main__":
    create_new_user()
