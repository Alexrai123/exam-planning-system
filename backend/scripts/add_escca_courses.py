"""
Script to add Echipamente si sisteme de comanda si control pentru autovehicule courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_escca_courses():
    """
    Add Echipamente si sisteme de comanda si control pentru autovehicule courses to the database
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
            
            # Get specialization ID for ESCCA
            result = conn.execute(text(
                "SELECT id, name, short_name FROM specializations WHERE short_name = 'ESCA' AND faculty_id = '1'"
            ))
            escca_spec = result.fetchone()
            
            if escca_spec:
                print(f"Found ESCCA specialization with ID: {escca_spec[0]}, Name: {escca_spec[1]}, Short Name: {escca_spec[2]}")
                escca_spec_id = escca_spec[0]
            else:
                print("ESCCA specialization not found")
                return
            
            # Define ESCCA Year 1 courses from the first image
            escca_year1_courses = [
                {"name": "Analiza matematica", "year": 1, "semester": 1},
                {"name": "Geometrie descriptiva", "year": 1, "semester": 1},
                {"name": "Chimie", "year": 1, "semester": 1},
                {"name": "Stiinta si ingineria materialelor", "year": 1, "semester": 1},
                {"name": "Programarea calculatoarelor si limbaje de programare", "year": 1, "semester": 1},
                {"name": "Economie generala", "year": 1, "semester": 1},
                {"name": "Fizica", "year": 1, "semester": 1},
                {"name": "Limbi moderne I", "year": 1, "semester": 1},
                {"name": "Educatie fizica si sport I", "year": 1, "semester": 1},
                {"name": "Algebra liniara, geometrie analitica si diferentiala", "year": 1, "semester": 2},
                {"name": "Desen tehnic si infografica I", "year": 1, "semester": 2},
                {"name": "Informatica aplicata", "year": 1, "semester": 2},
                {"name": "Metode numerice", "year": 1, "semester": 2},
                {"name": "Tehnologia materialelor", "year": 1, "semester": 2},
                {"name": "Mecanica", "year": 1, "semester": 2},
                {"name": "Comunicare", "year": 1, "semester": 2},
                {"name": "Limbi moderne II", "year": 1, "semester": 2},
                {"name": "Educatie fizica si sport II", "year": 1, "semester": 2}
            ]
            
            # Define ESCCA Year 2 courses from the second image
            escca_year2_courses = [
                {"name": "Matematici speciale", "year": 2, "semester": 1},
                {"name": "Rezistenta materialelor I", "year": 2, "semester": 1},
                {"name": "Mecanisme", "year": 2, "semester": 1},
                {"name": "Mecanisme - proiect", "year": 2, "semester": 1},
                {"name": "Control dimensional si masuratori tehnice", "year": 2, "semester": 1},
                {"name": "Electrotehnica si masini electrice I", "year": 2, "semester": 1},
                {"name": "Desen tehnic si infografica II", "year": 2, "semester": 1},
                {"name": "Educatie fizica si sport III", "year": 2, "semester": 1},
                {"name": "Limbi moderne 3", "year": 2, "semester": 2},
                {"name": "Rezistenta materialelor II", "year": 2, "semester": 2},
                {"name": "Metoda elementului finit", "year": 2, "semester": 2},
                {"name": "Electrotehnica si masini electrice II", "year": 2, "semester": 2},
                {"name": "Electronica aplicata I", "year": 2, "semester": 2},
                {"name": "Termotehnica", "year": 2, "semester": 2},
                {"name": "Bazele ingineriei autovehiculelor", "year": 2, "semester": 2},
                {"name": "Educatie fizica si sport IV", "year": 2, "semester": 2},
                {"name": "Limbi moderne IV", "year": 2, "semester": 2},
                {"name": "Practica de domeniu", "year": 2, "semester": 2}
            ]
            
            # Define ESCCA Year 3 courses from the third image
            escca_year3_courses = [
                {"name": "Organe de masini", "year": 3, "semester": 1},
                {"name": "Dinamica autovehiculelor I", "year": 3, "semester": 1},
                {"name": "Electronica aplicata II", "year": 3, "semester": 1},
                {"name": "Actionari hidraulice si pneumatice I", "year": 3, "semester": 1},
                {"name": "Procese si caracteristici ale motoarelor cu ardere interna", "year": 3, "semester": 1},
                {"name": "Sisteme automate pentru autovehicule", "year": 3, "semester": 1},
                {"name": "Echipament electric I", "year": 3, "semester": 1},
                {"name": "Electronica aplicata III", "year": 3, "semester": 2},
                {"name": "Echipament electric II", "year": 3, "semester": 2},
                {"name": "Masini electrice sisteme de propulsie si electronica de putere I", "year": 3, "semester": 2},
                {"name": "Microprocesoare si microcontrolere pentru sisteme de comanda pentru autovehicule I", "year": 3, "semester": 2},
                {"name": "Dinamica autovehiculelor II", "year": 3, "semester": 2},
                {"name": "Practica de specialitate", "year": 3, "semester": 2},
                {"name": "Proiectare asistata de calculator", "year": 3, "semester": 2},
                {"name": "Transmisii pentru autovehicule", "year": 3, "semester": 2},
                {"name": "Calculul si constructia automobilelor", "year": 3, "semester": 2},
                {"name": "Tehnologii neconventionale si de prelucrare mecanica", "year": 3, "semester": 2},
                {"name": "Software pentru ingineria autovehiculelor I", "year": 3, "semester": 2},
                {"name": "Mecanica autovehiculelor", "year": 3, "semester": 2},
                {"name": "Actionari hidraulice si pneumatice II", "year": 3, "semester": 2}
            ]
            
            # Define ESCCA Year 4 courses from the fourth image
            escca_year4_courses = [
                {"name": "Echipament electric pentru autovehicule", "year": 4, "semester": 1},
                {"name": "Sisteme de comanda si control pentru autovehicule I", "year": 4, "semester": 1},
                {"name": "Sisteme de comanda si control pentru autovehicule I - proiect", "year": 4, "semester": 1},
                {"name": "Proiectare asistata de calculator", "year": 4, "semester": 1},
                {"name": "Management", "year": 4, "semester": 1},
                {"name": "Masini electrice sisteme de propulsie si electronica de putere II", "year": 4, "semester": 1},
                {"name": "Microprocesoare si microcontrolere pentru sisteme de comanda pentru autovehicule II", "year": 4, "semester": 1},
                {"name": "Marketing", "year": 4, "semester": 1},
                {"name": "Fiabilitatea autovehiculelor", "year": 4, "semester": 2},
                {"name": "Sisteme telematice pentru transporturi rutiere", "year": 4, "semester": 2},
                {"name": "Retele si protocoale de comunicatii pentru autovehicule", "year": 4, "semester": 2},
                {"name": "Incercarea autovehiculelor", "year": 4, "semester": 2},
                {"name": "Tractiune electrica si hibrida II", "year": 4, "semester": 2},
                {"name": "Securitatea informatica a autovehiculelor", "year": 4, "semester": 2},
                {"name": "Software pentru ingineria autovehiculelor II", "year": 4, "semester": 2},
                {"name": "Compatibilitate electromagnetica pentru autovehicule", "year": 4, "semester": 2},
                {"name": "Sisteme de comanda si control pentru autovehicule II", "year": 4, "semester": 2},
                {"name": "Tehnici si echipamente de diagnosticare a autovehiculelor", "year": 4, "semester": 2}
            ]
            
            # Combine all courses
            all_escca_courses = escca_year1_courses + escca_year2_courses + escca_year3_courses + escca_year4_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding ESCCA courses to the database...")
            print("-" * 80)
            
            for course in all_escca_courses:
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
            print(f"Added {courses_added} new ESCCA courses to the database")
            
            # List ESCCA courses by year
            for year in range(1, 5):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '1' AND year = :year
                    AND name IN (
                        SELECT name FROM courses 
                        WHERE name LIKE '%autovehicul%'
                        OR name LIKE '%Chimie%'
                        OR name LIKE '%Mecanica%'
                        OR name LIKE '%Mecanisme%'
                        OR name LIKE '%Organe de masini%'
                        OR name LIKE '%Dinamica%'
                        OR name LIKE '%Actionari%'
                        OR name LIKE '%Echipament electric%'
                        OR name LIKE '%Masini electrice%'
                        OR name LIKE '%Microprocesoare%'
                        OR name LIKE '%Transmisii%'
                        OR name LIKE '%Tractiune%'
                        OR name LIKE '%Compatibilitate%'
                        OR name LIKE '%Fiabilitate%'
                        OR name LIKE '%Incercare%'
                        OR name LIKE '%Tehnici%'
                        OR name LIKE '%Securitate%'
                        OR name LIKE '%Sisteme de comanda%'
                        OR name LIKE '%Telematice%'
                    )
                    ORDER BY semester, name
                    """
                ), {"year": year})
                rows = result.fetchall()
                
                print(f"\nESCCA Year {year} courses in database ({len(rows)}):")
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
        print(f"Error adding ESCCA courses: {e}")

if __name__ == "__main__":
    add_escca_courses()
