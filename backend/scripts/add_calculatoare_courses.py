"""
Script to add Calculatoare (Computer Science) courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_calculatoare_courses():
    """
    Add Calculatoare (Computer Science) courses to the database
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
            
            # Get specialization ID for Calculatoare
            result = conn.execute(text(
                "SELECT id, name, short_name FROM specializations WHERE short_name = 'CALC' AND faculty_id = '1'"
            ))
            calc_spec = result.fetchone()
            
            if calc_spec:
                print(f"Found Calculatoare specialization with ID: {calc_spec[0]}, Name: {calc_spec[1]}, Short Name: {calc_spec[2]}")
                calc_spec_id = calc_spec[0]
            else:
                print("Calculatoare specialization not found")
                return
            
            # Define Calculatoare Year 1 courses from the first image
            calculatoare_year1_courses = [
                {"name": "Algebra liniara, geometrie analitica si diferentiala", "year": 1, "semester": 1},
                {"name": "Analiza matematica", "year": 1, "semester": 1},
                {"name": "Proiectare logica", "year": 1, "semester": 1},
                {"name": "Grafica asistata de calculator", "year": 1, "semester": 1},
                {"name": "Programarea calculatoarelor si limbaje de programare 1", "year": 1, "semester": 1},
                {"name": "Comunicare", "year": 1, "semester": 1},
                {"name": "Limba engleza 1", "year": 1, "semester": 1},
                {"name": "Educatie fizica si sport 1", "year": 1, "semester": 1},
                {"name": "Matematici speciale", "year": 1, "semester": 2},
                {"name": "Fizica 1", "year": 1, "semester": 2},
                {"name": "Programarea calculatoarelor si limbaje de programare 2", "year": 1, "semester": 2},
                {"name": "Arhitectura sistemelor de calcul", "year": 1, "semester": 2},
                {"name": "Electrotehnica", "year": 1, "semester": 2},
                {"name": "Limba engleza 2", "year": 1, "semester": 2}
            ]
            
            # Define Calculatoare Year 2 courses from the second image
            calculatoare_year2_courses = [
                {"name": "Dispozitive electronice si electronica analogica 1", "year": 2, "semester": 1},
                {"name": "Programare orientata pe obiecte", "year": 2, "semester": 1},
                {"name": "Fizica 2", "year": 2, "semester": 1},
                {"name": "Teoria sistemelor", "year": 2, "semester": 1},
                {"name": "Retele de calculatoare", "year": 2, "semester": 1},
                {"name": "Structura si organizarea calculatoarelor", "year": 2, "semester": 1},
                {"name": "Educatie fizica si sport III", "year": 2, "semester": 1},
                {"name": "Programarea interfetelor utilizator", "year": 2, "semester": 2},
                {"name": "Metode numerice", "year": 2, "semester": 2},
                {"name": "Programarea calculatoarelor si limbaje de programare 3", "year": 2, "semester": 2},
                {"name": "Masurari electronice, senzori si traductoare", "year": 2, "semester": 2},
                {"name": "Dispozitive electronice si electronica analogica 2", "year": 2, "semester": 2},
                {"name": "Proiectarea aplicatiilor orientate pe obiecte (proiect)", "year": 2, "semester": 2},
                {"name": "Electronica digitala", "year": 2, "semester": 2},
                {"name": "Practica in domeniu (30 ore)", "year": 2, "semester": 2}
            ]
            
            # Define Calculatoare Year 3 courses from the third image
            calculatoare_year3_courses = [
                {"name": "Structuri de date si algoritmi", "year": 3, "semester": 1},
                {"name": "Elemente de grafica pe calculator", "year": 3, "semester": 1},
                {"name": "Microcontrolere", "year": 3, "semester": 1},
                {"name": "Protocoale de comunicatii", "year": 3, "semester": 1},
                {"name": "Sisteme de operare", "year": 3, "semester": 1},
                {"name": "Elemente de grafica pe calculator - proiect", "year": 3, "semester": 1},
                {"name": "Microcontrolere - proiect", "year": 3, "semester": 1},
                {"name": "Proiectarea aplicatiilor WEB", "year": 3, "semester": 2},
                {"name": "Proiectarea algoritmilor", "year": 3, "semester": 2},
                {"name": "Baze de date", "year": 3, "semester": 2},
                {"name": "Baze de date - proiect", "year": 3, "semester": 2},
                {"name": "Inteligenta artificiala", "year": 3, "semester": 2},
                {"name": "Limba engleza IV", "year": 3, "semester": 2},
                {"name": "Practica de specialitate - 90 ore", "year": 3, "semester": 2},
                {"name": "Prelucrarea numerica a imaginilor", "year": 3, "semester": 2},
                {"name": "Procesoare numerice de semnal", "year": 3, "semester": 2}
            ]
            
            # Define Calculatoare Year 4 courses from the fourth image
            calculatoare_year4_courses = [
                {"name": "Sisteme inteligente", "year": 4, "semester": 1},
                {"name": "Sisteme de intrare-iesire si echipamente periferice", "year": 4, "semester": 1},
                {"name": "Ingineria programelor", "year": 4, "semester": 1},
                {"name": "Recunoasterea formelor", "year": 4, "semester": 1},
                {"name": "Circuite VLSI", "year": 4, "semester": 1},
                {"name": "Arhitecturi si prelucrari paralele", "year": 4, "semester": 1},
                {"name": "Practica pentru proiectul de diploma", "year": 4, "semester": 1},
                {"name": "Elaborarea proiectului de diploma", "year": 4, "semester": 2},
                {"name": "Proiectarea bazelor de date", "year": 4, "semester": 2},
                {"name": "Proiectarea asistata de calculator a modulelor electronice", "year": 4, "semester": 2},
                {"name": "Proiectarea translatoarelor", "year": 4, "semester": 2},
                {"name": "Sisteme de calcul in timp real", "year": 4, "semester": 2},
                {"name": "Calcul mobil", "year": 4, "semester": 2},
                {"name": "Sisteme cu microprocesoare", "year": 4, "semester": 2},
                {"name": "Aplicatii integrate pentru intreprinderi", "year": 4, "semester": 2},
                {"name": "Internetul obiectelor", "year": 4, "semester": 2},
                {"name": "Criptografie si securitate informationala", "year": 4, "semester": 2},
                {"name": "Domotica si cladiri inteligente", "year": 4, "semester": 2}
            ]
            
            # Combine all courses
            all_calculatoare_courses = calculatoare_year1_courses + calculatoare_year2_courses + calculatoare_year3_courses + calculatoare_year4_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding Calculatoare courses to the database...")
            print("-" * 80)
            
            for course in all_calculatoare_courses:
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
            print(f"Added {courses_added} new Calculatoare courses to the database")
            
            # List Calculatoare courses by year
            for year in range(1, 5):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '1' AND year = :year
                    ORDER BY semester, name
                    """
                ), {"year": year})
                rows = result.fetchall()
                
                print(f"\nCalculatoare Year {year} courses in database ({len(rows)}):")
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
        print(f"Error adding Calculatoare courses: {e}")

if __name__ == "__main__":
    add_calculatoare_courses()
