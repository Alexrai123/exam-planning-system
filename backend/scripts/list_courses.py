"""
Script to list all courses in the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.course import Course

def list_all_courses():
    """
    List all courses in the database
    """
    db = next(get_db())
    try:
        courses = db.query(Course).all()
        print(f"Found {len(courses)} courses in the database:")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<40} {'Professor':<30}")
        print("-" * 80)
        for course in courses:
            print(f"{course.id:<5} {course.name:<40} {course.profesor_name:<30}")
        print("-" * 80)
    except Exception as e:
        print(f"Error retrieving courses: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_all_courses()
