from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from datetime import date, time
import sys

# Add the backend directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import models after adding to path
from app.models.exam import Exam, ExamStatus
from app.models.course import Course
from app.models.sala import Sala
from app.models.grupa import Grupa
from app.models.user import User

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/exam_planning")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_test_exam():
    try:
        # Check if we have the necessary data
        course = db.query(Course).first()
        if not course:
            print("No courses found. Please create a course first.")
            return
        
        room = db.query(Sala).first()
        if not room:
            print("No rooms found. Please create a room first.")
            return
        
        group = db.query(Grupa).first()
        if not group:
            print("No groups found. Please create a group first.")
            return
        
        # Create a test exam
        exam = Exam(
            course_id=course.id,
            sala_id=room.id,
            grupa_id=group.id,
            date=date(2025, 6, 15),  # Example date
            time=time(10, 0),        # Example time (10:00 AM)
            status=ExamStatus.PROPOSED
        )
        
        db.add(exam)
        db.commit()
        db.refresh(exam)
        
        print(f"Test exam created successfully with ID: {exam.id}")
        print(f"Course: {course.name}")
        print(f"Room: {room.name}")
        print(f"Group: {group.name}")
        print(f"Date: {exam.date}")
        print(f"Time: {exam.time}")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating test exam: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_exam()
