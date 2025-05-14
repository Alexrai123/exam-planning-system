"""
Script to add Asistenta Medicala Generala Year 4 courses to the database with truncated names
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_amg_year4_courses_truncated():
    """
    Add Asistenta Medicala Generala Year 4 courses to the database with truncated names
    """
    try:
        # Define AMG Year 4 courses from the image (without numbers and with truncated names)
        amg_year4_courses = [
            # First semester courses
            {"name": "Procesul de imbatranire - Particularitatile pacientului geriatric", "year": 4, "semester": 1},
            {"name": "Examenul clinic si neuromotor al pacientului geriatric", "year": 4, "semester": 1},
            {"name": "Modalitatile terapeutice utilizate in recuperarea pacientilor geriatrici", "year": 4, "semester": 1},
            {"name": "Ingrijirea pacientului geriatric - Accidentul vascular", "year": 4, "semester": 1},
            {"name": "Ingrijirea pacientului geriatric - B. Parkinson", "year": 4, "semester": 1},
            {"name": "Ingrijirea pacientului geriatric - Neuropatia periferica", "year": 4, "semester": 1},
            {"name": "Ingrijirea pacientului geriatric - Scleroza multipla. B. Alzheimer", "year": 4, "semester": 1},
            
            # Second semester courses
            {"name": "Ingrijirea pacientului geriatric cu afectiuni cardio-vasculare", "year": 4, "semester": 2},
            {"name": "Ingrijirea pacientului geriatric - Artrita reumatoida", "year": 4, "semester": 2},
            {"name": "Ingrijirea pacientului geriatric - Artropatiile seronegative", "year": 4, "semester": 2},
            {"name": "Ingrijirea pacientului geriatric cu afectiuni articulare degenerative", "year": 4, "semester": 2},
            {"name": "Ingrijirea pacientului geriatric cu afectiuni gastro-enterologice", "year": 4, "semester": 2},
            {"name": "Ingrijirea pacientului geriatric oncologic", "year": 4, "semester": 2},
            {"name": "Procesul de imbatranire - Life Extension", "year": 4, "semester": 2}
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
            print("\nAdding AMG Year 4 courses to the database...")
            print("-" * 80)
            
            for course in amg_year4_courses:
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
            print(f"Added {courses_added} new AMG Year 4 courses to the database")
            
            # List all AMG Year 4 courses
            result = conn.execute(text(
                """
                SELECT id, name, year, semester 
                FROM courses 
                WHERE faculty_id = '21' AND year = 4
                ORDER BY year, semester, name
                """
            ))
            rows = result.fetchall()
            
            print(f"\nAMG Year 4 courses in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<65} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1][:65]} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 80)
            
            # List all AMG courses (all years)
            result = conn.execute(text(
                """
                SELECT year, COUNT(*) as course_count
                FROM courses 
                WHERE faculty_id = '21' 
                GROUP BY year
                ORDER BY year
                """
            ))
            year_counts = result.fetchall()
            
            print(f"\nAMG courses summary by year:")
            print("-" * 80)
            print(f"{'Year':<5} {'Course Count':<15}")
            print("-" * 80)
            
            for row in year_counts:
                print(f"{row[0]:<5} {row[1]:<15}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding AMG Year 4 courses: {e}")

if __name__ == "__main__":
    add_amg_year4_courses_truncated()
