from passlib.context import CryptContext
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/exam_planning")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# The new password
new_password = "password"

# Hash the password
hashed_password = pwd_context.hash(new_password)

try:
    # Update the admin user's password
    db.execute(
        text("UPDATE users SET password = :password WHERE email = 'admin@example.com'"),
        {"password": hashed_password}
    )
    db.commit()
    print(f"Password updated successfully for admin@example.com")
    print(f"New password hash: {hashed_password}")
    
    # Verify the password was updated
    result = db.execute(
        text("SELECT password FROM users WHERE email = 'admin@example.com'")
    ).scalar()
    print(f"Stored password hash: {result}")
    
    # Verify the new password works with the hash
    is_valid = pwd_context.verify(new_password, result)
    print(f"Password '{new_password}' matches the stored hash: {is_valid}")
    
except Exception as e:
    db.rollback()
    print(f"Error updating password: {e}")
finally:
    db.close()
