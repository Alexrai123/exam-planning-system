import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash

# Create a direct database connection
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/exam_planning"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# User email to update
email = "john.doe@student.usv.ro"
# Very simple password
new_password = "123456"

def set_password():
    print(f"Setting simple password for user: {email}")
    
    # Get DB session
    db = SessionLocal()
    
    try:
        # Check if user exists
        user_result = db.execute(
            text("SELECT id, name FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()
        
        if not user_result:
            print(f"User with email {email} not found")
            return False
            
        user_id, user_name = user_result
        
        # Hash the new password
        hashed_password = get_password_hash(new_password)
        
        # Update the password
        db.execute(
            text("UPDATE users SET password = :password WHERE id = :id"),
            {"password": hashed_password, "id": user_id}
        )
        
        # Commit changes
        db.commit()
        
        print(f"Password updated for {user_name} ({email})")
        print(f"New password: {new_password}")
        return True
            
    except Exception as e:
        db.rollback()
        print(f"Error setting password: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    set_password()
