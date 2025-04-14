from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User, UserRole
from app.core.security import get_password_hash
import sys

def create_test_users():
    # Create database engine and session
    db_url = str(settings.DATABASE_URL)
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if users already exist
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        professor = db.query(User).filter(User.email == "professor@example.com").first()
        student = db.query(User).filter(User.email == "student@example.com").first()
        
        # Create admin user if it doesn't exist
        if not admin:
            admin_user = User(
                name="Admin User",
                email="admin@example.com",
                password=get_password_hash("password"),
                role=UserRole.SECRETARIAT
            )
            db.add(admin_user)
            print("Created admin user")
        else:
            print("Admin user already exists")
        
        # Create professor user if it doesn't exist
        if not professor:
            professor_user = User(
                name="Professor User",
                email="professor@example.com",
                password=get_password_hash("password"),
                role=UserRole.PROFESSOR
            )
            db.add(professor_user)
            print("Created professor user")
        else:
            print("Professor user already exists")
        
        # Create student user if it doesn't exist
        if not student:
            student_user = User(
                name="Student User",
                email="student@example.com",
                password=get_password_hash("password"),
                role=UserRole.STUDENT
            )
            db.add(student_user)
            print("Created student user")
        else:
            print("Student user already exists")
        
        # Commit changes
        db.commit()
        print("All test users created successfully")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating test users: {e}", file=sys.stderr)
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()
