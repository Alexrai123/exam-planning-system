"""
Script to create a secretariat user with specific credentials
"""
from app.db.base import get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from sqlalchemy.orm import Session

def create_secretariat_user():
    # Get database connection
    db = next(get_db())
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == "secretariat@usv.ro").first()
    
    if existing_user:
        print(f"User with email secretariat@usv.ro already exists with ID: {existing_user.id}")
        return
    
    # Create password hash
    password_hash = get_password_hash("secretariat123")
    
    # Create new user
    new_user = User(
        name="Secretariat USV",
        email="secretariat@usv.ro",
        password=password_hash,
        role=UserRole.SECRETARIAT
    )
    
    # Add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"Created secretariat user with ID: {new_user.id}")
    print("Email: secretariat@usv.ro")
    print("Password: secretariat123")

if __name__ == "__main__":
    create_secretariat_user()
