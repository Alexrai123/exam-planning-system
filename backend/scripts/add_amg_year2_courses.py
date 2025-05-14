"""
Script to add Asistenta Medicala Generala Year 2 courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_amg_year2_courses():
    """
    Add Asistenta Medicala Generala Year 2 courses to the database
    """
    try:
        # Define AMG Year 2 courses from the image (without numbers)
        amg_year2_courses = [
            # First semester courses
            {"name": "Introducere in semiologie", "year": 2, "semester": 1},
            {"name": "Semiologie generala: pozitie, atitudine, facies", "year": 2, "semester": 1},
            {"name": "Semiologia tesutului subcutanat: stare hidratare, tesut adipos", "year": 2, "semester": 1},
            {"name": "Semiologia tesutului subcutanat: leziuni cutanate", "year": 2, "semester": 1},
            {"name": "Semiologia aparatului respirator-evaluare clinica si paraclinica. Tulburari ventilatorii", "year": 2, "semester": 1},
            {"name": "Semiologia aparatului respirator: sindroame de condensare; abcesul pulmonar", "year": 2, "semester": 1},
            {"name": "Semiologia aparatului respirator: sindroame obstructive, pulmonare", "year": 2, "semester": 1},
            
            # Second semester courses
            {"name": "Semiologia aparatului cardio- vascular: semne si simptome cardio-vasculare", "year": 2, "semester": 2},
            {"name": "Semiologia aparatului cardio-vascular: ECG normala si patologica. Tulburari de ritm, conducere", "year": 2, "semester": 2},
            {"name": "Semiologia aparatului cardio-vascular: valvulopatii, HTA", "year": 2, "semester": 2},
            {"name": "Semiologia aparatului cardio-vascular: angina pectorala", "year": 2, "semester": 2},
            {"name": "Semiologia aparatului cardio-vascular: infarctul miocardic", "year": 2, "semester": 2},
            {"name": "Semiologia aparatului cardio-vascular: boli vasculare periferice, tromboze", "year": 2, "semester": 2}
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
            print("\nAdding AMG Year 2 courses to the database...")
            print("-" * 80)
            
            for course in amg_year2_courses:
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
            print(f"Added {courses_added} new AMG Year 2 courses to the database")
            
            # List all AMG Year 2 courses
            result = conn.execute(text(
                """
                SELECT id, name, year, semester 
                FROM courses 
                WHERE faculty_id = '21' AND year = 2
                ORDER BY year, semester, name
                """
            ))
            rows = result.fetchall()
            
            print(f"\nAMG Year 2 courses in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<65} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<65} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 80)
            
            # List all AMG courses (Year 1 and 2)
            result = conn.execute(text(
                """
                SELECT id, name, year, semester 
                FROM courses 
                WHERE faculty_id = '21' 
                AND (
                    name LIKE 'Introducere in semiologie%'
                    OR name LIKE 'Semiologie%'
                    OR name LIKE 'Introducere, generalitati%'
                    OR name LIKE 'Dezvoltarea corpului uman%'
                    OR name LIKE 'Principii de organizare a corpului uman%'
                    OR name LIKE 'Sistemul%'
                    OR name LIKE 'Anatomie topografica%'
                )
                ORDER BY year, semester, name
                """
            ))
            rows = result.fetchall()
            
            print(f"\nAll AMG courses (Year 1 and 2) in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<65} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<65} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding AMG Year 2 courses: {e}")

if __name__ == "__main__":
    add_amg_year2_courses()
