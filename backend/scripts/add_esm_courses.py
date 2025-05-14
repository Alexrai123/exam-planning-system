"""
Script to add Echipamente si sisteme medicale (Medical Equipment and Systems) courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_esm_courses():
    """
    Add Echipamente si sisteme medicale (Medical Equipment and Systems) courses to the database
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
            
            # Get specialization ID for ESM
            result = conn.execute(text(
                "SELECT id, name, short_name FROM specializations WHERE short_name = 'ESM' AND faculty_id = '1'"
            ))
            esm_spec = result.fetchone()
            
            if esm_spec:
                print(f"Found ESM specialization with ID: {esm_spec[0]}, Name: {esm_spec[1]}, Short Name: {esm_spec[2]}")
                esm_spec_id = esm_spec[0]
            else:
                print("ESM specialization not found")
                return
            
            # Define ESM Year 1 and 2 courses from the first image
            esm_year1_courses = [
                {"name": "Chimie", "year": 1, "semester": 1},
                {"name": "Programarea calculatoarelor si limbaje de programare", "year": 1, "semester": 1},
                {"name": "Analiza matematica", "year": 1, "semester": 1},
                {"name": "Algebra liniara, geometrie analitica si diferentiala", "year": 1, "semester": 1},
                {"name": "Grafica asistata de calculator", "year": 1, "semester": 1},
                {"name": "Sisteme biologice", "year": 1, "semester": 1},
                {"name": "Comunicare", "year": 1, "semester": 1},
                {"name": "Educatie fizica si sport I", "year": 1, "semester": 1},
                {"name": "Anatomie topografica si functionala", "year": 1, "semester": 2},
                {"name": "Metode numerice", "year": 1, "semester": 2},
                {"name": "Matematici speciale", "year": 1, "semester": 2},
                {"name": "Informatica aplicata", "year": 1, "semester": 2},
                {"name": "Fizica", "year": 1, "semester": 2},
                {"name": "Electrotehnica I", "year": 1, "semester": 2},
                {"name": "Limba engleza I", "year": 1, "semester": 2}
            ]
            
            esm_year2_courses = [
                {"name": "Biochimie", "year": 2, "semester": 1},
                {"name": "Biofizica", "year": 2, "semester": 1},
                {"name": "Teoria probabilitatilor si statistica matematica", "year": 2, "semester": 1},
                {"name": "Electrotehnica II", "year": 2, "semester": 1},
                {"name": "Informatica medicala", "year": 2, "semester": 1},
                {"name": "Electronica I", "year": 2, "semester": 1},
                {"name": "Educatie fizica si sport II", "year": 2, "semester": 1},
                {"name": "Limba engleza II", "year": 2, "semester": 2},
                {"name": "Electronica II", "year": 2, "semester": 2},
                {"name": "Biomateriale", "year": 2, "semester": 2},
                {"name": "Masurari si instrumentatie", "year": 2, "semester": 2},
                {"name": "Masurari si instrumentatie (proiect)", "year": 2, "semester": 2},
                {"name": "Aparate pentru testari de laborator", "year": 2, "semester": 2},
                {"name": "Fiziologie si patologie", "year": 2, "semester": 2},
                {"name": "Practica de domeniu", "year": 2, "semester": 2},
                {"name": "Mecanisme si elemente de mecanica fina", "year": 2, "semester": 2}
            ]
            
            # Define ESM Year 3 and 4 courses from the second image
            esm_year3_courses = [
                {"name": "Ergonomia aparatelor medicale", "year": 3, "semester": 1},
                {"name": "Aparate pentru terapia intensiva", "year": 3, "semester": 1},
                {"name": "Optica medcala si echipamente optice", "year": 3, "semester": 1},
                {"name": "Electronica medicala", "year": 3, "semester": 1},
                {"name": "Sisteme cu microprocesoare", "year": 3, "semester": 1},
                {"name": "Notiuni de chirurgie", "year": 3, "semester": 1},
                {"name": "Medicina interna", "year": 3, "semester": 1},
                {"name": "Bazele medicinii dentare", "year": 3, "semester": 2},
                {"name": "Bloc operator", "year": 3, "semester": 2},
                {"name": "Bloc operator - proiect", "year": 3, "semester": 2},
                {"name": "Echipamente pentrudiagnostic", "year": 3, "semester": 2},
                {"name": "Practica de specialitate", "year": 3, "semester": 2},
                {"name": "Instrumentar medical", "year": 3, "semester": 2},
                {"name": "Compatibilitate electromagnetica in sisteme medicale", "year": 3, "semester": 2},
                {"name": "Sisteme biomedicale inteligente", "year": 3, "semester": 2}
            ]
            
            esm_year4_courses = [
                {"name": "Fiabilitatea echipamentelor medicale", "year": 4, "semester": 1},
                {"name": "Fiabilitatea echipamentelor medicale - proiect", "year": 4, "semester": 1},
                {"name": "Sisteme de executie pentru aparatura medicala", "year": 4, "semester": 1},
                {"name": "Notiuni de chirurgie", "year": 4, "semester": 1},
                {"name": "Prelucrarea semnalelor biomedicale", "year": 4, "semester": 1},
                {"name": "Echipamente medicale cu radiatii", "year": 4, "semester": 1},
                {"name": "Limba engleza III", "year": 4, "semester": 1},
                {"name": "Bloc operator", "year": 4, "semester": 2},
                {"name": "Etica si deontologie in inginerie medicala", "year": 4, "semester": 2},
                {"name": "Neurostiinte", "year": 4, "semester": 2},
                {"name": "Instrumentatie virtuala pentru medicina", "year": 4, "semester": 2},
                {"name": "Practica pentru proiectul de diploma", "year": 4, "semester": 2},
                {"name": "Elaborarea proiectului de diploma", "year": 4, "semester": 2},
                {"name": "Telemedicina", "year": 4, "semester": 2},
                {"name": "Sisteme de imagistica medicala", "year": 4, "semester": 2}
            ]
            
            # Combine all courses
            all_esm_courses = esm_year1_courses + esm_year2_courses + esm_year3_courses + esm_year4_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding ESM courses to the database...")
            print("-" * 80)
            
            for course in all_esm_courses:
                # Ensure course name is not longer than 100 characters
                if len(course["name"]) > 100:
                    original_name = course["name"]
                    course["name"] = course["name"][:97] + "..."
                    print(f"Truncated course name from '{original_name}' to '{course['name']}'")
                
                # Check if course already exists
                result = conn.execute(text(
                    "SELECT id FROM courses WHERE name = :name AND faculty_id = '1'"
                ), {"name": course["name"]})
                
                if result.rowcount == 0:
                    # Add course with faculty_id 1 (FIESC) and N/A professor
                    conn.execute(text(
                        """
                        INSERT INTO courses (name, profesor_name, faculty_id, year, semester) 
                        VALUES (:name, :profesor_name, :faculty_id, :year, :semester)
                        """
                    ), {
                        "name": course["name"],
                        "profesor_name": placeholder,
                        "faculty_id": "1",
                        "year": course["year"],
                        "semester": course["semester"]
                    })
                    
                    courses_added += 1
                    print(f"Added: {course['name']} (Year {course['year']}, Semester {course['semester']})")
                else:
                    print(f"Course already exists: {course['name']}")
            
            conn.commit()
            print("-" * 80)
            print(f"Added {courses_added} new ESM courses to the database")
            
            # List ESM courses by year
            for year in range(1, 5):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '1' AND year = :year
                    AND name IN (
                        SELECT name FROM courses 
                        WHERE name LIKE '%medical%'
                        OR name LIKE '%Anatomie%'
                        OR name LIKE '%Biochimie%'
                        OR name LIKE '%Biofizica%'
                        OR name LIKE '%Biomaterial%'
                        OR name LIKE '%Chirurgie%'
                        OR name LIKE '%Fiziologie%'
                        OR name LIKE '%Bloc operator%'
                        OR name LIKE '%Telemedicina%'
                        OR name LIKE '%Neurostiinte%'
                        OR name LIKE '%Etica%'
                        OR name LIKE '%Medicina%'
                        OR name LIKE '%Instrumentar%'
                        OR name LIKE '%Imagistica%'
                        OR name LIKE '%Optica%'
                        OR name LIKE '%Terapia%'
                        OR name LIKE '%Diagnostic%'
                        OR name LIKE '%Radiatii%'
                    )
                    ORDER BY semester, name
                    """
                ), {"year": year})
                rows = result.fetchall()
                
                print(f"\nESM Year {year} courses in database ({len(rows)}):")
                print("-" * 80)
                print(f"{'ID':<5} {'Name':<70} {'Year':<5} {'Semester':<5}")
                print("-" * 80)
                
                for row in rows:
                    print(f"{row[0]:<5} {row[1][:70]} {row[2]:<5} {row[3]:<5}")
                
                print("-" * 80)
            
            # Summary of all courses by year
            result = conn.execute(text(
                """
                SELECT year, COUNT(*) as course_count
                FROM courses 
                WHERE faculty_id = '1'
                GROUP BY year
                ORDER BY year
                """
            ))
            year_counts = result.fetchall()
            
            print(f"\nAll FIESC courses summary by year:")
            print("-" * 80)
            print(f"{'Year':<5} {'Course Count':<15}")
            print("-" * 80)
            
            for row in year_counts:
                print(f"{row[0]:<5} {row[1]:<15}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding ESM courses: {e}")

if __name__ == "__main__":
    add_esm_courses()
