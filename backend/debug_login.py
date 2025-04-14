import psycopg2
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

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

def verify_password(plain_password, hashed_password):
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Generate a password hash"""
    return pwd_context.hash(password)

def debug_login():
    """Debug login issues by checking users in the database"""
    print("Debugging login issues...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'users'
        )
    """)
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        print("ERROR: 'users' table does not exist!")
        return
    
    # Get all users
    cursor.execute("SELECT id, name, email, password, role FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("ERROR: No users found in the database!")
        return
    
    print(f"Found {len(users)} users in the database:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[4]}")
    
    # Test login with a test user
    test_email = "admin@example.com"
    test_password = "password"
    
    cursor.execute("SELECT id, email, password FROM users WHERE email = %s", (test_email,))
    user = cursor.fetchone()
    
    if not user:
        print(f"User with email {test_email} not found. Creating test user...")
        
        # Create a test user
        hashed_password = get_password_hash(test_password)
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, ("Admin User", test_email, hashed_password, "SECRETARIAT"))
        
        user_id = cursor.fetchone()[0]
        print(f"Created test user with ID: {user_id}")
        
        # Verify the user was created
        cursor.execute("SELECT id, email, password FROM users WHERE email = %s", (test_email,))
        user = cursor.fetchone()
    
    if user:
        print(f"Found user with email {test_email}")
        # Test password verification
        cursor.execute("SELECT password FROM users WHERE email = %s", (test_email,))
        hashed_password = cursor.fetchone()[0]
        
        is_valid = verify_password(test_password, hashed_password)
        print(f"Password verification result: {is_valid}")
        
        if not is_valid:
            print("Updating password for test user...")
            new_hashed_password = get_password_hash(test_password)
            cursor.execute("""
                UPDATE users
                SET password = %s
                WHERE email = %s
            """, (new_hashed_password, test_email))
            print(f"Password updated for user {test_email}")
    
    conn.close()
    
    print("\nLogin debugging completed!")
    print(f"You can now try to login with:")
    print(f"Email: {test_email}")
    print(f"Password: {test_password}")

if __name__ == "__main__":
    debug_login()
