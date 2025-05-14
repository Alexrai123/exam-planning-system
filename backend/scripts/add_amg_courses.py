"""
Script to add Asistenta Medicala Generala courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_amg_courses():
    """
    Add Asistenta Medicala Generala courses to the database
    """
    try:
        # Define AMG courses from the image (without numbers)
        amg_courses = [
            # First semester courses
            {"name": "Introducere, generalități, embriologie generală", "year": 1, "semester": 1},
            {"name": "Dezvoltarea corpului uman. Organogeneza. Fertilizarea. Perioada embrionară. Perioada fetală. Anexele fetale. Teratogeneza", "year": 1, "semester": 1},
            {"name": "Principii de organizare a corpului uman. Sistemul locomotor - generalități despre oase și articulații. Generalități despre mușchi și structurile conjunctive organizate conexe", "year": 1, "semester": 1},
            {"name": "Sistemul respirator. Organizarea funcțională a căilor respiratorii superioare, a arborelui bronhopulmonar", "year": 1, "semester": 1},
            {"name": "Sistemul cardiac. Sistemul circulator. Sistemul limfatic. Cordul - configurație externă și structură anatomică. Mica și marea circulație. Circulația limfatică. Organizarea morfo-funcțională a sistemului limfopoietic. Splina", "year": 1, "semester": 1},
            {"name": "Sistemul digestiv (I). Organizarea funcțională a tubului digestiv supra și sub-diafragmatic", "year": 1, "semester": 1},
            {"name": "Sistemul digestiv (II). Glandele anexe ale tubului digestiv", "year": 1, "semester": 1},
            
            # Second semester courses
            {"name": "Sistemul urinar. Organizarea funcțională a rinichiului și a căilor urinare", "year": 1, "semester": 2},
            {"name": "Sistemul de reproducere. Organizarea funcțională a gonadelor și a căilor genitale la bărbat", "year": 1, "semester": 2},
            {"name": "Sistemul de reproducere. Organizarea funcțională a gonadelor și a căilor genitale la femeie", "year": 1, "semester": 2},
            {"name": "Sistemul endocrin. Substratul morfologic al funcției endocrine. Organizarea funcțională a principalelor glande endocrine", "year": 1, "semester": 2},
            {"name": "Sistemul nervos. Principii de organizare funcțională a sistemului nervos central", "year": 1, "semester": 2},
            {"name": "Sistemul nervos. Principii de organizare funcțională a sistemului nervos periferic", "year": 1, "semester": 2},
            {"name": "Sistemul digestiv (III). Organizarea funcțională a organelor de simț", "year": 1, "semester": 2},
            {"name": "Anatomie topografică și secțională", "year": 1, "semester": 2}
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
                    print(f"Added: {course['name'][:70]}...")
                else:
                    print(f"Course already exists: {course['name'][:70]}...")
            
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
                    WHERE name LIKE 'Introducere, generalități%'
                    OR name LIKE 'Dezvoltarea corpului uman%'
                    OR name LIKE 'Principii de organizare a corpului uman%'
                    OR name LIKE 'Sistemul respirator%'
                    OR name LIKE 'Sistemul cardiac%'
                    OR name LIKE 'Sistemul digestiv%'
                    OR name LIKE 'Sistemul urinar%'
                    OR name LIKE 'Sistemul de reproducere%'
                    OR name LIKE 'Sistemul endocrin%'
                    OR name LIKE 'Sistemul nervos%'
                    OR name LIKE 'Anatomie topografică%'
                )
                ORDER BY year, semester, name
                """
            ))
            rows = result.fetchall()
            
            print(f"\nAMG courses in database ({len(rows)}):")
            print("-" * 100)
            print(f"{'ID':<5} {'Name':<80} {'Year':<5} {'Semester':<5}")
            print("-" * 100)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1][:80]} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 100)
        
    except Exception as e:
        print(f"Error adding AMG courses: {e}")

if __name__ == "__main__":
    add_amg_courses()
