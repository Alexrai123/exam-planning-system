"""
Script to add Medicina courses with shortened names
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_medicina_courses_simple():
    """
    Add Medicina courses with shortened names
    """
    try:
        # Define Medicina courses with shortened names
        medicina_courses = [
            # From image 1
            {"name": "C1. Obiectul Anatomiei", "year": 1, "semester": 1},
            {"name": "C2. Anatomia descriptiva, principii", "year": 1, "semester": 1},
            {"name": "C3. Prima saptamana a dezvoltarii", "year": 1, "semester": 1},
            {"name": "C4. Embriogeneza in saptamanile 4-8", "year": 1, "semester": 1},
            {"name": "C5. Dinamica morfofunctionala a anexelor embriofeale", "year": 1, "semester": 1},
            {"name": "C6. Cresterea si dezvoltarea sistemului locomotor", "year": 1, "semester": 1},
            {"name": "C7. Anatomia articulatiilor centurii membrului superior", "year": 1, "semester": 1},
            {"name": "C8. Anatomia articulatiilor radioulnara", "year": 1, "semester": 1},
            {"name": "C9. Anatomia articulatiilor centurii membrului inferior", "year": 1, "semester": 1},
            {"name": "C10. Anatomia articulatiilor membrului inferior", "year": 1, "semester": 1},
            
            # From image 2
            {"name": "C11. Dezvoltarea sistemului respirator", "year": 1, "semester": 2},
            {"name": "C12. Principii de organizare a sistemului respirator", "year": 1, "semester": 2},
            {"name": "C13. Dezvoltarea cordului", "year": 1, "semester": 2},
            {"name": "C14. Dezvoltarea sistemului vascular", "year": 1, "semester": 2}
        ]
        
        with engine.connect() as conn:
            # Check if N/A professor exists, create if needed
            placeholder = "N/A"
            result = conn.execute(text(
                "SELECT name FROM professors WHERE name = :name"
            ), {"name": placeholder})
            
            if result.rowcount == 0:
                conn.execute(text(
                    "INSERT INTO professors (name, faculty) VALUES (:name, 'N/A')"
                ), {"name": placeholder})
                print(f"Created placeholder professor: {placeholder}")
            
            # Add courses
            courses_added = 0
            print("\nAdding Medicina courses with shortened names...")
            print("-" * 80)
            
            for course in medicina_courses:
                # Check if course already exists
                result = conn.execute(text(
                    "SELECT id FROM courses WHERE name = :name"
                ), {"name": course["name"]})
                
                if result.rowcount == 0:
                    # Add course with faculty_id 21 (FMSB) and N/A professor
                    conn.execute(text(
                        """
                        INSERT INTO courses (name, profesor_name, faculty_id, year, semester) 
                        VALUES (:name, :profesor_name, :faculty_id, :year, :semester)
                        """
                    ), {
                        "name": course["name"],
                        "profesor_name": placeholder,
                        "faculty_id": "21",
                        "year": course["year"],
                        "semester": course["semester"]
                    })
                    
                    courses_added += 1
                    print(f"Added: {course['name']}")
                else:
                    print(f"Course already exists: {course['name']}")
            
            conn.commit()
            print("-" * 80)
            print(f"Added {courses_added} new Medicina courses to the database")
            
            # List all Medicina courses
            result = conn.execute(text(
                "SELECT id, name, year, semester FROM courses WHERE faculty_id = '21' ORDER BY year, semester, name"
            ))
            rows = result.fetchall()
            
            print(f"\nAll Medicina courses in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<50} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding Medicina courses: {e}")

if __name__ == "__main__":
    add_medicina_courses_simple()
