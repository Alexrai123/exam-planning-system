"""
Script to add Balneofiziokinetoterapie si recuperare (BFKT) Year 1 courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_bfkt_year1_courses():
    """
    Add Balneofiziokinetoterapie si recuperare (BFKT) Year 1 courses to the database
    """
    try:
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
            
            # Get specialization ID for BFKT
            result = conn.execute(text(
                "SELECT id, name, short_name FROM specializations WHERE short_name = 'BFKT'"
            ))
            bfkt_spec = result.fetchone()
            
            if bfkt_spec:
                print(f"Found BFKT specialization with ID: {bfkt_spec[0]}, Name: {bfkt_spec[1]}, Short Name: {bfkt_spec[2]}")
                bfkt_spec_id = bfkt_spec[0]
            else:
                print("BFKT specialization not found")
                return
            
            # Define BFKT Year 1 courses from the provided list
            # Assuming first half is semester 1, second half is semester 2
            bfkt_year1_courses = [
                # First semester courses
                {"name": "Obiectul Anatomiei. Istoric. Nomenclatura anatomica. Axe si planuri ale corpului uman", "year": 1, "semester": 1},
                {"name": "Aparat locomotor - Introducere in osteologie", "year": 1, "semester": 1},
                {"name": "Aparatul locomotor - Introducere in miologie", "year": 1, "semester": 1},
                {"name": "Aparatul locomotor - Introducere in artrologie", "year": 1, "semester": 1},
                {"name": "Oasele si articulatiile neurocraniului", "year": 1, "semester": 1},
                {"name": "Oasele si articulatiile viscerocraniului", "year": 1, "semester": 1},
                {"name": "Muschii capului si gatului", "year": 1, "semester": 1},
                
                # Second semester courses
                {"name": "Anatomia peretilor trunchiului", "year": 1, "semester": 2},
                {"name": "Structura peretelui abdominal", "year": 1, "semester": 2},
                {"name": "Anatomie descriptiva. Vascularizatia arteriala a membrului superior", "year": 1, "semester": 2},
                {"name": "Anatomie descriptiva. Vascularizatia venoasa si limfatica a membrului superior", "year": 1, "semester": 2},
                {"name": "Anatomie descriptiva. Inervatia membrului superior", "year": 1, "semester": 2},
                {"name": "Anatomie descriptiva. Vascularizatia arteriala a membrului inferior", "year": 1, "semester": 2},
                {"name": "Anatomie descriptiva. Inervatia membrului inferior", "year": 1, "semester": 2}
            ]
            
            # Add courses
            courses_added = 0
            print("\nAdding BFKT Year 1 courses to the database...")
            print("-" * 80)
            
            for course in bfkt_year1_courses:
                # Check if course already exists
                result = conn.execute(text(
                    "SELECT id FROM courses WHERE name = :name AND faculty_id = '21'"
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
                    print(f"Added: {course['name']} (Year {course['year']}, Semester {course['semester']})")
                else:
                    print(f"Course already exists: {course['name']}")
            
            conn.commit()
            print("-" * 80)
            print(f"Added {courses_added} new BFKT Year 1 courses to the database")
            
            # List BFKT Year 1 courses by semester
            for semester in range(1, 3):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '21' AND year = 1 AND semester = :semester
                    AND name IN (
                        SELECT name FROM courses 
                        WHERE name LIKE 'Obiectul Anatomiei%'
                        OR name LIKE 'Aparat locomotor%'
                        OR name LIKE 'Aparatul locomotor%'
                        OR name LIKE 'Oasele%'
                        OR name LIKE 'Muschii%'
                        OR name LIKE 'Anatomia%'
                        OR name LIKE 'Structura%'
                        OR name LIKE 'Anatomie descriptiva%'
                    )
                    ORDER BY id
                    """
                ), {"semester": semester})
                rows = result.fetchall()
                
                print(f"\nBFKT Year 1, Semester {semester} courses in database ({len(rows)}):")
                print("-" * 80)
                print(f"{'ID':<5} {'Name':<70} {'Year':<5} {'Semester':<5}")
                print("-" * 80)
                
                for row in rows:
                    print(f"{row[0]:<5} {row[1][:70]} {row[2]:<5} {row[3]:<5}")
                
                print("-" * 80)
        
    except Exception as e:
        print(f"Error adding BFKT Year 1 courses: {e}")

if __name__ == "__main__":
    add_bfkt_year1_courses()
