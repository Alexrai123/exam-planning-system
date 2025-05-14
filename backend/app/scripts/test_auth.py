import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.security import verify_password

# Create a direct database connection
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/exam_planning"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test user credentials
email = "john.doe@student.usv.ro"
password = "password123"

def test_auth():
    print(f"Testing authentication for user: {email}")
    
    # Get DB session
    db = SessionLocal()
    
    try:
        # Get user from database
        user_result = db.execute(
            text("SELECT id, name, email, password, role FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()
        
        if not user_result:
            print(f"User with email {email} not found in database")
            return False
            
        user_id, user_name, user_email, hashed_password, user_role = user_result
        
        print(f"Found user: {user_name} (ID: {user_id}, Role: {user_role})")
        
        # Verify password
        is_password_correct = verify_password(password, hashed_password)
        
        if is_password_correct:
            print("Password verification successful!")
            return True
        else:
            print("Password verification failed!")
            print(f"Provided password: {password}")
            print(f"Stored hashed password: {hashed_password}")
            return False
            
    except Exception as e:
        print(f"Error during authentication test: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_auth()
