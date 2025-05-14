"""
Script to create test accounts for professor and admin roles
"""
from app.db.base import get_db, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.professor import Professor
import sys

def create_test_accounts():
    """Create test accounts for professor and admin roles"""
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if professor user already exists
        professor_email = "john.smith@usv.ro"
        existing_professor = db.query(User).filter(User.email == professor_email).first()
        
        if not existing_professor:
            print(f"Creating professor user with email: {professor_email}")
            # Create password hash
            password_hash = get_password_hash("password123")
            
            # Create new professor user
            new_professor = User(
                name="John Smith",
                email=professor_email,
                password=password_hash,
                role=UserRole.PROFESSOR
            )
            
            db.add(new_professor)
            db.flush()  # Flush to get the ID
            
            # Check if professor exists in professors table
            professor = db.query(Professor).filter(Professor.name == "John Smith").first()
            
            if not professor:
                # Create professor record
                professor = Professor(
                    name="John Smith",
                    specialization="Computer Science",
                    title="PhD",
                    email=professor_email,
                    user_id=new_professor.id
                )
                db.add(professor)
            else:
                # Link existing professor to user
                professor.user_id = new_professor.id
                professor.email = professor_email
            
            print(f"Professor user created with ID: {new_professor.id}")
        else:
            print(f"Professor user already exists with ID: {existing_professor.id}")
        
        # Check if admin user already exists
        admin_email = "admin@usv.ro"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if not existing_admin:
            print(f"Creating admin user with email: {admin_email}")
            # Create password hash
            password_hash = get_password_hash("password123")
            
            # Create new admin user
            new_admin = User(
                name="Admin User",
                email=admin_email,
                password=password_hash,
                role=UserRole.ADMIN
            )
            
            db.add(new_admin)
            print(f"Admin user created")
        else:
            print(f"Admin user already exists with ID: {existing_admin.id}")
        
        # Commit changes
        db.commit()
        print("All accounts created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating test accounts: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_test_accounts()
