"""
Script to add Balneofiziokinetoterapie si recuperare (BFKT) courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_bfkt_courses():
    """
    Add Balneofiziokinetoterapie si recuperare (BFKT) courses to the database
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
            
            # Define BFKT Year 1 courses
            bfkt_year1_courses = [
                # First semester courses
                {"name": "Anatomie functionala", "year": 1, "semester": 1},
                {"name": "Biomecanica", "year": 1, "semester": 1},
                {"name": "Bazele kinetoterapiei", "year": 1, "semester": 1},
                {"name": "Fiziologie generala", "year": 1, "semester": 1},
                {"name": "Biofizica", "year": 1, "semester": 1},
                {"name": "Psihologie medicala", "year": 1, "semester": 1},
                {"name": "Educatie fizica medicala", "year": 1, "semester": 1},
                
                # Second semester courses
                {"name": "Anatomie functionala si biomecanica", "year": 1, "semester": 2},
                {"name": "Fiziologia efortului", "year": 1, "semester": 2},
                {"name": "Tehnici de manevrare a pacientului", "year": 1, "semester": 2},
                {"name": "Electroterapie", "year": 1, "semester": 2},
                {"name": "Masaj terapeutic", "year": 1, "semester": 2},
                {"name": "Evaluare functionala in kinetoterapie", "year": 1, "semester": 2},
                {"name": "Metode de cercetare in BFKT", "year": 1, "semester": 2}
            ]
            
            # Define BFKT Year 2 courses
            bfkt_year2_courses = [
                # First semester courses
                {"name": "Kinetoterapia in afectiuni neurologice", "year": 2, "semester": 1},
                {"name": "Kinetoterapia in afectiuni ortopedice", "year": 2, "semester": 1},
                {"name": "Kinetoterapia in afectiuni reumatologice", "year": 2, "semester": 1},
                {"name": "Kinetoterapia in geriatrie", "year": 2, "semester": 1},
                {"name": "Hidroterapie", "year": 2, "semester": 1},
                {"name": "Termoterapie", "year": 2, "semester": 1},
                {"name": "Fizioterapie", "year": 2, "semester": 1},
                
                # Second semester courses
                {"name": "Kinetoterapia in afectiuni cardiovasculare", "year": 2, "semester": 2},
                {"name": "Kinetoterapia in afectiuni respiratorii", "year": 2, "semester": 2},
                {"name": "Kinetoterapia in pediatrie", "year": 2, "semester": 2},
                {"name": "Kinetoterapia in traumatologie sportiva", "year": 2, "semester": 2},
                {"name": "Balneologie", "year": 2, "semester": 2},
                {"name": "Terapie ocupationala", "year": 2, "semester": 2},
                {"name": "Practica clinica", "year": 2, "semester": 2}
            ]
            
            # Define BFKT Year 3 courses
            bfkt_year3_courses = [
                # First semester courses
                {"name": "Recuperare medicala in afectiuni neurologice", "year": 3, "semester": 1},
                {"name": "Recuperare medicala in afectiuni ortopedice", "year": 3, "semester": 1},
                {"name": "Recuperare medicala in afectiuni reumatologice", "year": 3, "semester": 1},
                {"name": "Recuperare medicala post-traumatica", "year": 3, "semester": 1},
                {"name": "Tehnici speciale de kinetoterapie", "year": 3, "semester": 1},
                {"name": "Metode de evaluare in recuperarea medicala", "year": 3, "semester": 1},
                {"name": "Stagiu clinic", "year": 3, "semester": 1},
                
                # Second semester courses
                {"name": "Recuperare medicala in afectiuni cardiovasculare", "year": 3, "semester": 2},
                {"name": "Recuperare medicala in afectiuni respiratorii", "year": 3, "semester": 2},
                {"name": "Recuperare medicala in afectiuni pediatrice", "year": 3, "semester": 2},
                {"name": "Recuperare medicala in geriatrie", "year": 3, "semester": 2},
                {"name": "Tehnici complementare in recuperarea medicala", "year": 3, "semester": 2},
                {"name": "Metode de cercetare in recuperarea medicala", "year": 3, "semester": 2},
                {"name": "Practica pentru elaborarea lucrarii de licenta", "year": 3, "semester": 2}
            ]
            
            # Combine all courses
            all_bfkt_courses = bfkt_year1_courses + bfkt_year2_courses + bfkt_year3_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding BFKT courses to the database...")
            print("-" * 80)
            
            for course in all_bfkt_courses:
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
            print(f"Added {courses_added} new BFKT courses to the database")
            
            # List BFKT courses by year
            for year in range(1, 4):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '21' AND year = :year
                    AND name IN (
                        SELECT name FROM courses 
                        WHERE name LIKE 'Anatomie functionala%'
                        OR name LIKE 'Biomecanica%'
                        OR name LIKE 'Kinetoterapia%'
                        OR name LIKE 'Recuperare medicala%'
                        OR name LIKE 'Fizioterapie%'
                        OR name LIKE 'Electroterapie%'
                        OR name LIKE 'Masaj%'
                        OR name LIKE 'Hidroterapie%'
                        OR name LIKE 'Balneologie%'
                        OR name LIKE 'Termoterapie%'
                        OR name LIKE 'Tehnici%'
                        OR name LIKE 'Evaluare%'
                        OR name LIKE 'Practica%'
                        OR name LIKE 'Stagiu%'
                        OR name LIKE 'Metode%'
                        OR name LIKE 'Terapie%'
                        OR name LIKE 'Bazele%'
                    )
                    ORDER BY semester, name
                    """
                ), {"year": year})
                rows = result.fetchall()
                
                print(f"\nBFKT Year {year} courses in database ({len(rows)}):")
                print("-" * 80)
                print(f"{'ID':<5} {'Name':<60} {'Year':<5} {'Semester':<5}")
                print("-" * 80)
                
                for row in rows:
                    print(f"{row[0]:<5} {row[1]:<60} {row[2]:<5} {row[3]:<5}")
                
                print("-" * 80)
            
            # Summary of all BFKT courses
            result = conn.execute(text(
                """
                SELECT year, COUNT(*) as course_count
                FROM courses 
                WHERE faculty_id = '21'
                AND name IN (
                    SELECT name FROM courses 
                    WHERE name LIKE 'Anatomie functionala%'
                    OR name LIKE 'Biomecanica%'
                    OR name LIKE 'Kinetoterapia%'
                    OR name LIKE 'Recuperare medicala%'
                    OR name LIKE 'Fizioterapie%'
                    OR name LIKE 'Electroterapie%'
                    OR name LIKE 'Masaj%'
                    OR name LIKE 'Hidroterapie%'
                    OR name LIKE 'Balneologie%'
                    OR name LIKE 'Termoterapie%'
                    OR name LIKE 'Tehnici%'
                    OR name LIKE 'Evaluare%'
                    OR name LIKE 'Practica%'
                    OR name LIKE 'Stagiu%'
                    OR name LIKE 'Metode%'
                    OR name LIKE 'Terapie%'
                    OR name LIKE 'Bazele%'
                )
                GROUP BY year
                ORDER BY year
                """
            ))
            year_counts = result.fetchall()
            
            print(f"\nBFKT courses summary by year:")
            print("-" * 80)
            print(f"{'Year':<5} {'Course Count':<15}")
            print("-" * 80)
            
            for row in year_counts:
                print(f"{row[0]:<5} {row[1]:<15}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding BFKT courses: {e}")

if __name__ == "__main__":
    add_bfkt_courses()
