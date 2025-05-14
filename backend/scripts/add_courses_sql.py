"""
Script to add courses to the database using raw SQL
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_courses_sql():
    """
    Add courses to the database using raw SQL
    """
    try:
        # Define simple courses for Medicina
        medicina_courses = [
            {"name": "Anatomie", "profesor_name": "Prof. Dr. Ionescu", "faculty_id": "21", "year": 1, "semester": 1},
            {"name": "Fiziologie", "profesor_name": "Prof. Dr. Popescu", "faculty_id": "21", "year": 1, "semester": 2},
            {"name": "Biochimie", "profesor_name": "Prof. Dr. Georgescu", "faculty_id": "21", "year": 1, "semester": 1}
        ]
        
        with engine.connect() as conn:
            # Check if professors exist, create if needed
            for course in medicina_courses:
                prof_name = course["profesor_name"]
                
                # Check if professor exists
                result = conn.execute(text(
                    "SELECT name FROM professors WHERE name = :name"
                ), {"name": prof_name})
                
                if result.rowcount == 0:
                    # Create professor
                    conn.execute(text(
                        "INSERT INTO professors (name, faculty) VALUES (:name, :faculty)"
                    ), {"name": prof_name, "faculty": "Facultatea de Medicină și Științe Biologice"})
                    print(f"Created professor: {prof_name}")
            
            # Add courses
            courses_added = 0
            print("\nAdding courses to the database...")
            print("-" * 80)
            
            for course in medicina_courses:
                # Check if course already exists
                result = conn.execute(text(
                    "SELECT id FROM courses WHERE name = :name"
                ), {"name": course["name"]})
                
                if result.rowcount == 0:
                    # Add course
                    conn.execute(text(
                        """
                        INSERT INTO courses (name, profesor_name, faculty_id, year, semester) 
                        VALUES (:name, :profesor_name, :faculty_id, :year, :semester)
                        """
                    ), course)
                    
                    courses_added += 1
                    print(f"Added course: {course['name']}")
                else:
                    print(f"Course already exists: {course['name']}")
            
            conn.commit()
            print("-" * 80)
            print(f"Added {courses_added} new courses to the database")
            
            # List all courses for faculty 21
            result = conn.execute(text(
                "SELECT id, name, profesor_name, year, semester FROM courses WHERE faculty_id = '21'"
            ))
            rows = result.fetchall()
            
            print(f"\nCourses for FMSB (Faculty ID 21) in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<30} {'Professor':<30} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<30} {row[2]:<30} {row[3]:<5} {row[4]:<5}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding courses: {e}")

if __name__ == "__main__":
    add_courses_sql()
