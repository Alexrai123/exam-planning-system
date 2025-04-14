from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import DictCursor

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

# Sample password to set for all users
sample_password = "password123"
hashed_password = pwd_context.hash(sample_password)

def update_passwords():
    """Update all user passwords with a properly hashed version"""
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        # Update all user passwords
        cursor.execute("UPDATE users SET password = %s", (hashed_password,))
        
        # Commit the changes
        conn.commit()
        
        # Get the count of updated users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        print(f"Successfully updated passwords for {user_count} users.")
        print(f"Sample password for all users: {sample_password}")
        
        # Close the connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error updating passwords: {e}")

if __name__ == "__main__":
    update_passwords()
