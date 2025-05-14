"""
Script to add Automatica si informatica aplicata (Automation and Applied Computer Science) courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_automatica_courses():
    """
    Add Automatica si informatica aplicata (Automation and Applied Computer Science) courses to the database
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
            
            # Get specialization ID for Automatica si informatica aplicata
            result = conn.execute(text(
                "SELECT id, name, short_name FROM specializations WHERE short_name = 'AIA' AND faculty_id = '1'"
            ))
            aia_spec = result.fetchone()
            
            if aia_spec:
                print(f"Found Automatica si informatica aplicata specialization with ID: {aia_spec[0]}, Name: {aia_spec[1]}, Short Name: {aia_spec[2]}")
                aia_spec_id = aia_spec[0]
            else:
                print("Automatica si informatica aplicata specialization not found")
                return
            
            # Define Automatica Year 1 courses from the first image
            automatica_year1_courses = [
                {"name": "Analiza matematica", "year": 1, "semester": 1},
                {"name": "Algebra liniara, geometrie analitica si diferentiala", "year": 1, "semester": 1},
                {"name": "Analiza si sinteza dispozitivelor numerice", "year": 1, "semester": 1},
                {"name": "Programarea calculatoarelor si limbaje de programare I", "year": 1, "semester": 1},
                {"name": "Grafica asistata pe calculator", "year": 1, "semester": 1},
                {"name": "Tehnologie electronica", "year": 1, "semester": 1},
                {"name": "Educatie fizica si sport I", "year": 1, "semester": 1},
                {"name": "Matematici speciale", "year": 1, "semester": 2},
                {"name": "Fizica I", "year": 1, "semester": 2},
                {"name": "Programarea calculatoarelor si limbaje de programare II", "year": 1, "semester": 2},
                {"name": "Electrotehnica", "year": 1, "semester": 2},
                {"name": "Arhitectura calculatoarelor", "year": 1, "semester": 2},
                {"name": "Comunicare", "year": 1, "semester": 2},
                {"name": "Limba engleza I", "year": 1, "semester": 2},
                {"name": "Limba straina tehnica I - Engleza", "year": 1, "semester": 2},
                {"name": "Limba straina tehnica I - Franceza", "year": 1, "semester": 2},
                {"name": "Limba straina tehnica I - Germana", "year": 1, "semester": 2},
                {"name": "Complemente de matematica", "year": 1, "semester": 2},
                {"name": "Limba straina tehnica II - Engleza", "year": 1, "semester": 2},
                {"name": "Limba straina tehnica II - Franceza", "year": 1, "semester": 2},
                {"name": "Limba straina tehnica II - Germana", "year": 1, "semester": 2},
                {"name": "Teoria probabilitatilor si statistica matematica", "year": 1, "semester": 2}
            ]
            
            # Define Automatica Year 2 courses from the second image
            automatica_year2_courses = [
                {"name": "Circuite electronice liniare I", "year": 2, "semester": 1},
                {"name": "Programarea calculatoarelor si limbaje de programare III", "year": 2, "semester": 1},
                {"name": "Teoria sistemelor I", "year": 2, "semester": 1},
                {"name": "Fizica II", "year": 2, "semester": 1},
                {"name": "Sisteme dinamice cu evenimente discrete", "year": 2, "semester": 1},
                {"name": "Sisteme cu microprocesoare", "year": 2, "semester": 1},
                {"name": "Educatie fizica si sport II", "year": 2, "semester": 1},
                {"name": "Metode numerice", "year": 2, "semester": 2},
                {"name": "Electronica digitala", "year": 2, "semester": 2},
                {"name": "Masurari si traductoare", "year": 2, "semester": 2},
                {"name": "Circuite electronice liniare II", "year": 2, "semester": 2},
                {"name": "Teoria sistemelor II", "year": 2, "semester": 2},
                {"name": "Limbaje de asamblare", "year": 2, "semester": 2},
                {"name": "Practica de domeniu", "year": 2, "semester": 2},
                {"name": "Limba straina tehnica III - Engleza", "year": 2, "semester": 2},
                {"name": "Limba straina tehnica III - Franceza", "year": 2, "semester": 2},
                {"name": "Limba straina tehnica III - Germana", "year": 2, "semester": 2},
                {"name": "Statistica economica", "year": 2, "semester": 2},
                {"name": "Limba straina tehnica IV - Engleza", "year": 2, "semester": 2},
                {"name": "Limba straina tehnica IV - Franceza", "year": 2, "semester": 2},
                {"name": "Limba straina tehnica IV - Germana", "year": 2, "semester": 2}
            ]
            
            # Define Automatica Year 3 courses from the third image
            automatica_year3_courses = [
                {"name": "Microcontrolere - arhitecturi si programare", "year": 3, "semester": 1},
                {"name": "Retele de calculatoare", "year": 3, "semester": 1},
                {"name": "Electronica de putere", "year": 3, "semester": 1},
                {"name": "Ingineria sistemelor automate", "year": 3, "semester": 1},
                {"name": "Modelare, identificare si simulare", "year": 3, "semester": 1},
                {"name": "Modelare, identificare si simulare (proiect)", "year": 3, "semester": 1},
                {"name": "Masini electrice si actionari", "year": 3, "semester": 1},
                {"name": "Baze de date", "year": 3, "semester": 2},
                {"name": "Sisteme de conducere a proceselor tehnologice", "year": 3, "semester": 2},
                {"name": "Optimizari", "year": 3, "semester": 2},
                {"name": "Limba engleza II", "year": 3, "semester": 2},
                {"name": "Practica de specialitate", "year": 3, "semester": 2},
                {"name": "Proiectare asistata de calculator", "year": 3, "semester": 2},
                {"name": "Sisteme de operare", "year": 3, "semester": 2},
                {"name": "Tehnici de securizare a informatiei", "year": 3, "semester": 2},
                {"name": "Prelucrarea semnalelor", "year": 3, "semester": 2},
                {"name": "Instrumentatie virtuala", "year": 3, "semester": 2},
                {"name": "Echipamente de automatizare electrice si electronice", "year": 3, "semester": 2},
                {"name": "Programare JAVA", "year": 3, "semester": 2},
                {"name": "Surse regenerabile", "year": 3, "semester": 2},
                {"name": "Competente antreprenoriale", "year": 3, "semester": 2},
                {"name": "Complemente de ingineria sistemelor", "year": 3, "semester": 2},
                {"name": "Drept si legislatie economica", "year": 3, "semester": 2},
                {"name": "Proiectarea algoritmilor", "year": 3, "semester": 2}
            ]
            
            # Define Automatica Year 4 courses from the fourth image
            automatica_year4_courses = [
                {"name": "Programarea aplicatiilor internet", "year": 4, "semester": 1},
                {"name": "Retele industriale de calculatoare", "year": 4, "semester": 1},
                {"name": "Managementul proiectelor", "year": 4, "semester": 1},
                {"name": "Sisteme de inteligenta artificiala distribuite", "year": 4, "semester": 1},
                {"name": "Circuite periferice si interfete de proces", "year": 4, "semester": 1},
                {"name": "Limba engleza III", "year": 4, "semester": 1},
                {"name": "Automate si microprogramare", "year": 4, "semester": 1},
                {"name": "Fiabilitate si diagnoza", "year": 4, "semester": 1},
                {"name": "Fiabilitate si diagnoza (proiect)", "year": 4, "semester": 1},
                {"name": "Elaborarea proiectului de diploma", "year": 4, "semester": 2},
                {"name": "Practica pentru proiectul de diploma", "year": 4, "semester": 2},
                {"name": "Sisteme de timp real", "year": 4, "semester": 2},
                {"name": "Conducerea structurilor flexibile de fabricatie", "year": 4, "semester": 2},
                {"name": "Retele neuronale si logica fuzzy", "year": 4, "semester": 2},
                {"name": "Sisteme de comanda si reglare a actionarilor electrice", "year": 4, "semester": 2},
                {"name": "Automatizarea cladirilor", "year": 4, "semester": 2},
                {"name": "Internetul obiectelor", "year": 4, "semester": 2},
                {"name": "Tehnici de programare cu baze de date", "year": 4, "semester": 2},
                {"name": "Circuite logice programabile", "year": 4, "semester": 2},
                {"name": "Proiectarea bazelor de date", "year": 4, "semester": 2},
                {"name": "Ingineria sistemelor de programe", "year": 4, "semester": 2},
                {"name": "Sisteme mobile", "year": 4, "semester": 2},
                {"name": "Inventica", "year": 4, "semester": 2}
            ]
            
            # Combine all courses
            all_automatica_courses = automatica_year1_courses + automatica_year2_courses + automatica_year3_courses + automatica_year4_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding Automatica si informatica aplicata courses to the database...")
            print("-" * 80)
            
            for course in all_automatica_courses:
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
            print(f"Added {courses_added} new Automatica si informatica aplicata courses to the database")
            
            # List Automatica courses by year
            for year in range(1, 5):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '1' AND year = :year
                    AND name IN (
                        SELECT name FROM courses 
                        WHERE name LIKE '%Automatica%'
                        OR name LIKE '%Analiza%'
                        OR name LIKE '%Algebra%'
                        OR name LIKE '%Programare%'
                        OR name LIKE '%Sisteme%'
                        OR name LIKE '%Microcontrolere%'
                        OR name LIKE '%Retele%'
                        OR name LIKE '%Electronica%'
                        OR name LIKE '%Ingineria%'
                        OR name LIKE '%Modelare%'
                        OR name LIKE '%Baze de date%'
                        OR name LIKE '%Optimizari%'
                        OR name LIKE '%Limba%'
                        OR name LIKE '%Practica%'
                        OR name LIKE '%Proiectare%'
                        OR name LIKE '%Tehnici%'
                        OR name LIKE '%Prelucrare%'
                        OR name LIKE '%Instrumentatie%'
                        OR name LIKE '%Echipamente%'
                        OR name LIKE '%JAVA%'
                        OR name LIKE '%Surse%'
                        OR name LIKE '%Competente%'
                        OR name LIKE '%Complemente%'
                        OR name LIKE '%Drept%'
                        OR name LIKE '%Algoritmi%'
                        OR name LIKE '%Internet%'
                        OR name LIKE '%Management%'
                        OR name LIKE '%Inteligenta%'
                        OR name LIKE '%Circuite%'
                        OR name LIKE '%Automate%'
                        OR name LIKE '%Fiabilitate%'
                        OR name LIKE '%Diploma%'
                        OR name LIKE '%Timp real%'
                        OR name LIKE '%Conducere%'
                        OR name LIKE '%Neuronale%'
                        OR name LIKE '%Comanda%'
                        OR name LIKE '%Cladiri%'
                        OR name LIKE '%Logice%'
                        OR name LIKE '%Mobile%'
                        OR name LIKE '%Inventica%'
                    )
                    ORDER BY semester, name
                    """
                ), {"year": year})
                rows = result.fetchall()
                
                print(f"\nAutomatica si informatica aplicata Year {year} courses in database ({len(rows)}):")
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
        print(f"Error adding Automatica si informatica aplicata courses: {e}")

if __name__ == "__main__":
    add_automatica_courses()
