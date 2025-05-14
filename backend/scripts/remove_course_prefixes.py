"""
Script to remove C1-C14 prefixes from Medicina course names
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def remove_course_prefixes():
    """
    Remove C1-C14 prefixes from Medicina course names
    """
    try:
        with engine.connect() as conn:
            # First, create a backup of the current courses
            conn.execute(text(
                "CREATE TABLE IF NOT EXISTS courses_backup_with_prefixes AS SELECT * FROM courses"
            ))
            print("Created backup of courses with prefixes as courses_backup_with_prefixes table")
            
            # Get all courses with C prefixes
            result = conn.execute(text(
                "SELECT id, name FROM courses WHERE name LIKE 'C_. %' OR name LIKE 'C__. %'"
            ))
            courses = result.fetchall()
            
            print("\nRemoving prefixes from course names...")
            print("-" * 80)
            
            # Update each course to remove the prefix
            for course_id, course_name in courses:
                # Extract the part after the prefix (after "C1. ", "C10. ", etc.)
                new_name = course_name.split(". ", 1)[1] if ". " in course_name else course_name
                
                # Update the course name
                conn.execute(text(
                    "UPDATE courses SET name = :new_name WHERE id = :id"
                ), {"new_name": new_name, "id": course_id})
                
                print(f"Updated: {course_name} -> {new_name}")
            
            conn.commit()
            print("-" * 80)
            print(f"Removed prefixes from {len(courses)} course names")
            
            # List all updated Medicina courses
            result = conn.execute(text(
                "SELECT id, name, year, semester FROM courses WHERE faculty_id = '21' ORDER BY year, semester, name"
            ))
            rows = result.fetchall()
            
            print(f"\nUpdated Medicina courses in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<50} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error removing course prefixes: {e}")

if __name__ == "__main__":
    remove_course_prefixes()
