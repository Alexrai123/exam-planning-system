import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create a direct database connection
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/exam_planning"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_fiesc_courses():
    print("Adding courses for FIESC faculty...")
    
    # Get DB session
    db = SessionLocal()
    
    try:
        # Check if FIESC faculty exists
        fiesc_faculty = db.execute(
            text("SELECT id, name FROM faculties WHERE name LIKE '%FIESC%'")
        ).fetchone()
        
        if not fiesc_faculty:
            # Create FIESC faculty if it doesn't exist
            result = db.execute(
                text("INSERT INTO faculties (name) VALUES ('FIESC') RETURNING id, name")
            )
            fiesc_faculty = result.fetchone()
            db.commit()
            print(f"Created new faculty: FIESC (ID: {fiesc_faculty[0]})")
        else:
            print(f"Found existing faculty: {fiesc_faculty[1]} (ID: {fiesc_faculty[0]})")
        
        faculty_id = fiesc_faculty[0]
        
        # Sample courses for FIESC faculty
        sample_courses = [
            "Introduction to Electrical Engineering",
            "Digital Electronics",
            "Power Systems",
            "Control Systems",
            "Microprocessors and Microcontrollers",
            "Signals and Systems",
            "Electrical Machines",
            "Power Electronics",
            "Communication Systems",
            "VLSI Design",
            "Computer Networks",
            "Embedded Systems",
            "Robotics",
            "Automation Systems",
            "Internet of Things"
        ]
        
        # Add courses for FIESC faculty
        added_courses = 0
        for course_name in sample_courses:
            # Check if course already exists
            existing_course = db.execute(
                text("SELECT id FROM courses WHERE name = :name"),
                {"name": course_name}
            ).fetchone()
            
            if not existing_course:
                # Add new course
                db.execute(
                    text("INSERT INTO courses (name, faculty_id) VALUES (:name, :faculty_id)"),
                    {"name": course_name, "faculty_id": faculty_id}
                )
                added_courses += 1
                print(f"Added course: {course_name}")
        
        db.commit()
        print(f"Added {added_courses} new courses to FIESC faculty")
        
        # Verify courses were added
        fiesc_courses = db.execute(
            text("SELECT id, name FROM courses WHERE faculty_id = :faculty_id"),
            {"faculty_id": faculty_id}
        ).fetchall()
        
        print(f"\nCourses for FIESC faculty (ID: {faculty_id}):")
        for course in fiesc_courses:
            course_id, course_name = course
            print(f"  - {course_name} (ID: {course_id})")
            
    except Exception as e:
        db.rollback()
        print(f"Error adding FIESC courses: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    add_fiesc_courses()
