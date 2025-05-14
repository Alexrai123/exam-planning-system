import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.db.base import get_db, Base, engine
from app.models.course import Course
from app.models.faculty import Faculty

# Sample courses for FIESC faculty
FIESC_COURSES = [
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

def main():
    # Get DB session
    db = next(get_db())
    
    try:
        # Check if FIESC faculty exists
        fiesc_faculty = db.query(Faculty).filter(Faculty.name.like("%FIESC%")).first()
        
        if not fiesc_faculty:
            print("FIESC faculty not found. Creating new faculty...")
            fiesc_faculty = Faculty(name="FIESC")
            db.add(fiesc_faculty)
            db.flush()  # This assigns an ID to the faculty
            print(f"Created new faculty: FIESC (ID: {fiesc_faculty.id})")
        else:
            print(f"Found existing faculty: {fiesc_faculty.name} (ID: {fiesc_faculty.id})")
        
        # Add courses for FIESC faculty
        added_courses = 0
        for course_name in FIESC_COURSES:
            # Check if course already exists
            existing_course = db.query(Course).filter(Course.name == course_name).first()
            
            if not existing_course:
                # Create new course
                new_course = Course(
                    name=course_name,
                    faculty_id=fiesc_faculty.id
                )
                db.add(new_course)
                db.flush()
                added_courses += 1
                print(f"Added course: {course_name} (ID: {new_course.id})")
        
        # Commit all changes
        db.commit()
        print(f"Added {added_courses} new courses to FIESC faculty")
        
        # Verify courses were added
        fiesc_courses = db.query(Course).filter(Course.faculty_id == fiesc_faculty.id).all()
        
        print(f"\nCourses for FIESC faculty (ID: {fiesc_faculty.id}):")
        for course in fiesc_courses:
            print(f"  - {course.name} (ID: {course.id})")
            
    except Exception as e:
        db.rollback()
        print(f"Error adding FIESC courses: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
