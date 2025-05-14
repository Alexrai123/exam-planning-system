"""
Script to add all Medicina courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_all_medicina_courses():
    """
    Add all Medicina courses to the database
    """
    try:
        # Define all Medicina courses from the images
        medicina_courses = [
            # From image 1
            {"name": "Obiectul Anatomiei: Istoric. Nomenclatura anatomica. Elemente de anatomie: macroscopica osteologica, musculofasciala si vasculonervosa", "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva, principii, etapele ontogenezei, terminologie. Gametogeneza la barbat intre perioada embrionara, prepubertara si viata adulta. Particularitatile morfogenezei gametelor maturi si femei. Spermatogeneza normala si patologica. Malformatii congenitale", "year": 1, "semester": 1},
            {"name": "Prima saptamana a dezvoltarii de la ovulatie la fertilizare si nidatie. Saptamana a doua a dezvoltarii (vezii embrionare). Discul embrionar bilaminat (didermis). Corelatii clinice. Saptamana a treia a dezvoltarii. Discul embrionar trilaminat", "year": 1, "semester": 1},
            {"name": "Embriogeneza in saptamanile 4-8. Delimitarea craniocaudala si laterolaterala. Morfogeneza structurilor specifice derivate din straturile germinative (ectoderm, endoderm, mezoderm). Corelatii clinice. Perioada fetala de la organogeneza la nastere", "year": 1, "semester": 1},
            {"name": "Dinamica morfofunctionala a anexelor embriofeale (membranelor fetale si placentei). Corelatii clinice", "year": 1, "semester": 1},
            {"name": "Cresterea si dezvoltarea sistemului locomotor (osteogeneza si al segmentului vertebral si planului axial. Corelatii clinice", "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor centurii membrului superior: articulatia sternoclaviculara, acromioclaviculara, sternocostala, articulatia glenohumerala. Corelatii clinice", "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor radioulnara proximala si distala, articulatia radiocarpiana. Membrana interosoasa antebrahiala. Articulatiile mainii. Corelatii clinice", "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor centurii membrului inferior: Articulatia pubica, articulatia sacroiliaca. Articulatia coxofemurala. Articulatia genunchiului. Corelatii clinice", "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor membrului inferior: Articulatiile tibiofibuloasa proximala si distala, articulatia talocrurorala, articulatiile piciorului. Corelatii clinice", "year": 1, "semester": 1},
            
            # From image 2
            {"name": "Dezvoltarea sistemului respirator. Morfogeneza sistemului respirator inferior (traheo-bronho-pneumo-alveolara). Maturarea planmonilor. Corelatii clinice", "year": 1, "semester": 2},
            {"name": "Principii de organizare a sistemului respirator. Subsisteme de ventilatie, perfuzie si difuziune. Organizarea functionala a mediastinului. Anatomia clinica", "year": 1, "semester": 2},
            {"name": "Dezvoltarea cordului. Localizarea ariei cardiogene. Formarea tubului si ansei cardiace. Dezvoltarea septelor cordului. Formarea sistemului vascular arterial si venos. Separarea cavitatilor cordului. Corelatii clinice", "year": 1, "semester": 2},
            {"name": "Dezvoltarea sistemului vascular. Circulatia fetala si definitiva. Principiu de organizare functionala a cordului si vaselor", "year": 1, "semester": 2}
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
            
            # Add courses
            courses_added = 0
            print("\nAdding all Medicina courses to the database...")
            print("-" * 80)
            
            for course in medicina_courses:
                # Check if course already exists
                result = conn.execute(text(
                    "SELECT id FROM courses WHERE name = :name"
                ), {"name": course["name"]})
                
                if result.rowcount == 0:
                    # Truncate course name to fit within 100 characters
                    truncated_name = course["name"][:97] + "..." if len(course["name"]) > 100 else course["name"]
                    
                    # Add course with faculty_id 21 (FMSB) and N/A professor
                    conn.execute(text(
                        """
                        INSERT INTO courses (name, profesor_name, faculty_id, year, semester) 
                        VALUES (:name, :profesor_name, :faculty_id, :year, :semester)
                        """
                    ), {
                        "name": truncated_name,
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
            print(f"Added {courses_added} new Medicina courses to the database")
            
            # List all Medicina courses
            result = conn.execute(text(
                "SELECT id, name, year, semester FROM courses WHERE faculty_id = '21' ORDER BY id"
            ))
            rows = result.fetchall()
            
            print(f"\nAll Medicina courses in database ({len(rows)}):")
            print("-" * 100)
            print(f"{'ID':<5} {'Name':<80} {'Year':<5} {'Semester':<5}")
            print("-" * 100)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1][:80]}... {row[2]:<5} {row[3]:<5}")
            
            print("-" * 100)
        
    except Exception as e:
        print(f"Error adding Medicina courses: {e}")

if __name__ == "__main__":
    add_all_medicina_courses()
