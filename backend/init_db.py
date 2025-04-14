from app.db.base import Base, engine
from app.models.user import User
from app.models.course import Course
from app.models.grupa import Grupa
from app.models.sala import Sala
from app.models.exam import Exam
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from app.db.base import SessionLocal

# Create tables
def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if we already have users
        user = db.query(User).first()
        if not user:
            print("Creating initial data...")
            
            # Create admin user
            admin = User(
                name="Admin User",
                email="admin@example.com",
                password=get_password_hash("password"),
                role="secretariat"
            )
            db.add(admin)
            
            # Create a professor
            professor = User(
                name="Professor User",
                email="professor@example.com",
                password=get_password_hash("password"),
                role="professor"
            )
            db.add(professor)
            
            # Create a student
            student = User(
                name="Student User",
                email="student@example.com",
                password=get_password_hash("password"),
                role="student"
            )
            db.add(student)
            
            # Commit users
            db.commit()
            
            # Create a course
            course = Course(
                name="Introduction to Computer Science",
                profesor_id=professor.id
            )
            db.add(course)
            db.commit()
            
            # Create a group
            group = Grupa(
                name="Group A"
            )
            db.add(group)
            db.commit()
            
            # Create a room
            room = Sala(
                name="Room 101"
            )
            db.add(room)
            db.commit()
            
            print("Initial data created successfully!")
        else:
            print("Database already contains data, skipping initialization")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created!")
