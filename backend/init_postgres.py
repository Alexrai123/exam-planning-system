import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.user import User
from app.core.config import settings
from app.core.security import get_password_hash

# Create engine and session
engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if we already have users
    user_count = db.query(User).count()
    if user_count == 0:
        print("Creating initial users...")
        
        # Create users
        admin = User(
            email="admin@example.com",
            password=get_password_hash("password"),
            full_name="Admin User",
            role="secretariat",
            is_active=True
        )
        
        professor = User(
            email="professor@example.com",
            password=get_password_hash("password"),
            full_name="Professor User",
            role="professor",
            is_active=True
        )
        
        student = User(
            email="student@example.com",
            password=get_password_hash("password"),
            full_name="Student User",
            role="student",
            is_active=True
        )
        
        db.add(admin)
        db.add(professor)
        db.add(student)
        db.commit()
        
        print("Initial users created successfully!")
    else:
        print("Database already contains users, skipping initialization.")
    
    db.close()

if __name__ == "__main__":
    print("Initializing the PostgreSQL database...")
    init_db()
    print("Database initialization completed!")
