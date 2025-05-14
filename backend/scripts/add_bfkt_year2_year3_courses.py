"""
Script to add Balneofiziokinetoterapie si recuperare (BFKT) Year 2 and Year 3 courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_bfkt_year2_year3_courses():
    """
    Add Balneofiziokinetoterapie si recuperare (BFKT) Year 2 and Year 3 courses to the database
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
            
            # Define BFKT Year 2 courses from the provided image
            bfkt_year2_courses = [
                {"name": "Obiectul de studiu al Kinetologiei (stiinta miscarii)", "year": 2, "semester": 1},
                {"name": "Tehnici in kinetologie - clasificare. Pozitii fundamentale si derivate", "year": 2, "semester": 1},
                {"name": "Cinematica, kinetica si relatia cu pozitiile-posturi, control, coordonare, echilibru", "year": 2, "semester": 1},
                {"name": "Mijloace fundamentale ale kinetologiei. Exercitiul fizic terapeutic", "year": 2, "semester": 1},
                {"name": "Mijloace specifice kinetologiei asociate exercitiului fizic", "year": 2, "semester": 1},
                {"name": "Procedee pentru stimularea aparatului respirator si a functiei respiratorii", "year": 2, "semester": 2},
                {"name": "Procedee pentru stimularea aparatului cardio-vascular si a functiilor acestuia", "year": 2, "semester": 2},
                {"name": "Procedee pentru stimularea functiei de nutritie", "year": 2, "semester": 2},
                {"name": "Obiective de baza in kinetologie. Cresterea fortei musculare", "year": 2, "semester": 2},
                {"name": "Cresterea rezistentei musculare. Relaxarea", "year": 2, "semester": 2},
                {"name": "Antrenamentul la efort. Reeducarea sensibilitatii", "year": 2, "semester": 2},
                {"name": "Cresterea mobilitatii articulare", "year": 2, "semester": 2},
                {"name": "Obiective de baza in kinetologie. Corectarea posturii si antrainmentului", "year": 2, "semester": 2}
            ]
            
            # Define BFKT Year 3 courses from the provided image
            bfkt_year3_courses = [
                {"name": "Metodologia cercetarii: introducere, obiective", "year": 3, "semester": 1},
                {"name": "Metoda stiintifica, procesul cercetarii stiintifice", "year": 3, "semester": 1},
                {"name": "Formularea de ipoteze, tipuri de ipoteze si caracteristici", "year": 3, "semester": 1},
                {"name": "Instrumentele cercetarii stiintifice", "year": 3, "semester": 1},
                {"name": "Etapele si intelegerea lucrarii stiintifice", "year": 3, "semester": 1},
                {"name": "Formularea problemei, identificarea in literatura", "year": 3, "semester": 1},
                {"name": "Folosirea tipurilor de studii variate", "year": 3, "semester": 1},
                {"name": "Notiuni de statistica experimentala", "year": 3, "semester": 2},
                {"name": "Experiment, experienta, modelarea experimentala", "year": 3, "semester": 2},
                {"name": "Factori de influenta si parametrii de optimizare", "year": 3, "semester": 2},
                {"name": "Elemente de statistica: atributuri, varianta, statistica descriptiva", "year": 3, "semester": 2},
                {"name": "Redactarea unei lucrari stiintifice. Meta-analiza", "year": 3, "semester": 2},
                {"name": "Aplicatii pentru grant: tipuri, finantare, continut aplicatie", "year": 3, "semester": 2},
                {"name": "Prezentarea rezultatelor cercetarii", "year": 3, "semester": 2}
            ]
            
            # Combine all courses
            all_bfkt_courses = bfkt_year2_courses + bfkt_year3_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding BFKT Year 2 and Year 3 courses to the database...")
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
            print(f"Added {courses_added} new BFKT Year 2 and Year 3 courses to the database")
            
            # List BFKT courses by year
            for year in range(2, 4):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '21' AND year = :year
                    ORDER BY semester, id
                    """
                ), {"year": year})
                rows = result.fetchall()
                
                print(f"\nBFKT Year {year} courses in database ({len(rows)}):")
                print("-" * 80)
                print(f"{'ID':<5} {'Name':<70} {'Year':<5} {'Semester':<5}")
                print("-" * 80)
                
                for row in rows:
                    print(f"{row[0]:<5} {row[1][:70]} {row[2]:<5} {row[3]:<5}")
                
                print("-" * 80)
            
            # Summary of all BFKT courses
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
            
            print(f"\nAll FMSB courses summary by year:")
            print("-" * 80)
            print(f"{'Year':<5} {'Course Count':<15}")
            print("-" * 80)
            
            for row in year_counts:
                print(f"{row[0]:<5} {row[1]:<15}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding BFKT Year 2 and Year 3 courses: {e}")

if __name__ == "__main__":
    add_bfkt_year2_year3_courses()
