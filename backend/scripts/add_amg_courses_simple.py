"""
Script to add Asistenta Medicala Generala courses to the database with simplified names
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_amg_courses_simple():
    """
    Add Asistenta Medicala Generala courses to the database with simplified names
    """
    try:
        # Define AMG courses from the image (without numbers and with simplified characters)
        amg_courses = [
            # First semester courses
            {"name": "Introducere, generalitati, embriologie generala", "year": 1, "semester": 1},
            {"name": "Dezvoltarea corpului uman. Organogeneza", "year": 1, "semester": 1},
            {"name": "Principii de organizare a corpului uman", "year": 1, "semester": 1},
            {"name": "Sistemul respirator", "year": 1, "semester": 1},
            {"name": "Sistemul cardiac. Sistemul circulator", "year": 1, "semester": 1},
            {"name": "Sistemul digestiv (I)", "year": 1, "semester": 1},
            {"name": "Sistemul digestiv (II)", "year": 1, "semester": 1},
            
            # Second semester courses
            {"name": "Sistemul urinar", "year": 1, "semester": 2},
            {"name": "Sistemul de reproducere (barbat)", "year": 1, "semester": 2},
            {"name": "Sistemul de reproducere (femeie)", "year": 1, "semester": 2},
            {"name": "Sistemul endocrin", "year": 1, "semester": 2},
            {"name": "Sistemul nervos central", "year": 1, "semester": 2},
            {"name": "Sistemul nervos periferic", "year": 1, "semester": 2},
            {"name": "Sistemul digestiv (III)", "year": 1, "semester": 2},
            {"name": "Anatomie topografica si sectionala", "year": 1, "semester": 2}
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
            
            # Get specialization ID for AMG
            result = conn.execute(text(
                "SELECT id FROM specializations WHERE short_name = 'AMG'"
            ))
            amg_spec_id = result.scalar()
            
            if amg_spec_id:
                print(f"Found AMG specialization with ID: {amg_spec_id}")
            else:
                print("AMG specialization not found")
            
            # Add courses
            courses_added = 0
            print("\nAdding AMG courses to the database...")
            print("-" * 80)
            
            for course in amg_courses:
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
            print(f"Added {courses_added} new AMG courses to the database")
            
            # List all AMG courses
            result = conn.execute(text(
                """
                SELECT id, name, year, semester 
                FROM courses 
                WHERE faculty_id = '21' 
                AND name IN (
                    SELECT name FROM courses 
                    WHERE name LIKE 'Introducere, generalitati%'
                    OR name LIKE 'Dezvoltarea corpului uman%'
                    OR name LIKE 'Principii de organizare a corpului uman%'
                    OR name LIKE 'Sistemul respirator%'
                    OR name LIKE 'Sistemul cardiac%'
                    OR name LIKE 'Sistemul digestiv%'
                    OR name LIKE 'Sistemul urinar%'
                    OR name LIKE 'Sistemul de reproducere%'
                    OR name LIKE 'Sistemul endocrin%'
                    OR name LIKE 'Sistemul nervos%'
                    OR name LIKE 'Anatomie topografica%'
                )
                ORDER BY year, semester, name
                """
            ))
            rows = result.fetchall()
            
            print(f"\nAMG courses in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<50} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding AMG courses: {e}")

if __name__ == "__main__":
    add_amg_courses_simple()
