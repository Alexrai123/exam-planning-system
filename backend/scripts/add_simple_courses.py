"""
Script to add simple courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import get_db
from app.models.course import Course

def add_simple_courses():
    """
    Add simple courses to the database
    """
    db = next(get_db())
    try:
        # Define simple courses
        simple_courses = [
            {"name": "Anatomie", "profesor_name": "Prof. Dr. Ionescu", "faculty_id": "21", "year": 1, "semester": 1},
            {"name": "Fiziologie", "profesor_name": "Prof. Dr. Popescu", "faculty_id": "21", "year": 1, "semester": 2},
            {"name": "Biochimie", "profesor_name": "Prof. Dr. Georgescu", "faculty_id": "21", "year": 1, "semester": 1}
        ]
        
        # Add courses to database
        courses_added = 0
        print("Adding simple courses to the database...")
        print("-" * 80)
        
        for course_data in simple_courses:
            # Check if course already exists
            existing_course = db.query(Course).filter(Course.name == course_data["name"]).first()
            if existing_course:
                print(f"Course already exists: {course_data['name']}")
            else:
                new_course = Course(**course_data)
                db.add(new_course)
                courses_added += 1
                print(f"Added: {course_data['name']}")
        
        # Commit changes
        db.commit()
        print("-" * 80)
        print(f"Added {courses_added} new courses to the database")
        
    except Exception as e:
        print(f"Error adding courses: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_simple_courses()
