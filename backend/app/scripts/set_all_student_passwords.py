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

# Email addresses of the group leaders
emails = [
    "john.doe@student.usv.ro",
    "jane.smith@student.usv.ro",
    "maria.popescu@student.usv.ro",
    "alexandru.ionescu@student.usv.ro",
    "elena.dumitrescu@student.usv.ro",
    "andrei.constantinescu@student.usv.ro",
    "cristina.georgescu@student.usv.ro",
    "mihai.stanescu@student.usv.ro",
    "laura.vasilescu@student.usv.ro",
    "bogdan.marinescu@student.usv.ro",
    "ana.petrescu@student.usv.ro"
]

# Very simple password
new_password = "123456"

def set_passwords():
    print(f"Setting simple password for all student accounts")
    
    # Get DB session
    db = SessionLocal()
    
    updated_users = 0
    errors = []
    
    # Hash the new password once
    hashed_password = get_password_hash(new_password)
    
    for email in emails:
        try:
            # Check if user exists
            user_result = db.execute(
                text("SELECT id, name FROM users WHERE email = :email"),
                {"email": email}
            ).fetchone()
            
            if not user_result:
                errors.append(f"User with email {email} not found")
                continue
                
            user_id, user_name = user_result
            
            # Update the password
            db.execute(
                text("UPDATE users SET password = :password WHERE id = :id"),
                {"password": hashed_password, "id": user_id}
            )
            
            updated_users += 1
            print(f"Password updated for {user_name} ({email})")
            
            # Commit changes for this user
            db.commit()
            
        except Exception as e:
            db.rollback()
            errors.append(f"Error setting password for {email}: {str(e)}")
            print(f"Error: {str(e)}")
    
    print(f"\nSummary:")
    print(f"Updated users: {updated_users}")
    print(f"New password for all users: {new_password}")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
    
    db.close()

if __name__ == "__main__":
    set_passwords()
