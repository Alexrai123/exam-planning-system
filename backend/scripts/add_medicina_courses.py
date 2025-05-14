"""
Script to add Medicina courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.base import get_db
from app.models.course import Course
from app.models.professor import Professor

def add_medicina_courses():
    """
    Add Medicina courses to the database
    """
    db = next(get_db())
    try:
        # Define professors first
        professors = [
            "Prof. Dr. Ionescu",
            "Prof. Dr. Popescu",
            "Prof. Dr. Georgescu",
            "Prof. Dr. Mihai",
            "Prof. Dr. Stoica",
            "Prof. Dr. Radu",
            "Prof. Dr. Vasilescu",
            "Prof. Dr. Dinu",
            "Prof. Dr. Marin",
            "Prof. Dr. Florescu",
            "Prof. Dr. Neagu",
            "Prof. Dr. Dragomir",
            "Prof. Dr. Stanescu",
            "Prof. Dr. Dumitrescu"
        ]
        
        # Add professors to database
        professors_added = 0
        print("Adding professors to the database...")
        print("-" * 80)
        
        for prof_name in professors:
            # Check if professor already exists
            existing_prof = db.query(Professor).filter(Professor.name == prof_name).first()
            if existing_prof:
                print(f"Professor already exists: {prof_name}")
            else:
                new_prof = Professor(name=prof_name, faculty="Facultatea de Medicină și Științe Biologice")
                db.add(new_prof)
                professors_added += 1
                print(f"Added professor: {prof_name}")
        
        # Commit professor changes
        db.commit()
        print("-" * 80)
        print(f"Added {professors_added} new professors to the database")
        print()
        
        # Define Medicina courses from the images
        medicina_courses = [
            # From image 1
            {"name": "Obiectul Anatomiei: Istoric. Nomenclatura anatomica. Elemente de anatomie: macroscopica osteologica, musculofasciala si vasculonervosa", "profesor_name": "Prof. Dr. Ionescu", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva, principii, etapele ontogenezei, terminologie. Gametogeneza la barbat intre perioada embrionara, prepubertara si viata adulta. Particularitatile morfogenezei gametelor maturi si femei. Spermatogeneza normala si patologica. Malformatii congenitale", "profesor_name": "Prof. Dr. Popescu", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Particularitatile dezvoltarii de la ovulatie la fertilizare si implantare. Dezvoltarea embrionului. Anexele fetale. Discul embrionar bilaminat (didermis). Corelații clinice. Structura si topografia placentei. Discul embrionar trilaminat. Corelații clinice", "profesor_name": "Prof. Dr. Georgescu", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Embriogeneza in saptamanile 4-8. Delimitarea craniocaudala si laterolaterala. Morfogeneza structurilor specifice derivate din straturile germinative (ectoderm, endoderm, mezoderm). Corelații clinice. Perioada fetala de la 9 saptamani la nastere", "profesor_name": "Prof. Dr. Mihai", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Dinamica morfofunctionala a anexelor embriofeale (membranelor fetale si placentei)", "profesor_name": "Prof. Dr. Stoica", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Cresterea si dezvoltarea sistemului locomotor (osteogeneza si al segmentului vertebral si planului axial", "profesor_name": "Prof. Dr. Radu", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor centurii membrului superior: articulatia sternoclaviculara, acromioclaviculara, sternocostala, articulatia glenohumerala", "profesor_name": "Prof. Dr. Vasilescu", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor radioulnara proximala si distala, articulatia radiocarpiana. Membrana interosoasa antebrahiala", "profesor_name": "Prof. Dr. Dinu", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor centurii membrului inferior: Articulatia pubica, articulatia sacroiliaca. Articulatia coxofemurala. Articulatia genunchiului", "profesor_name": "Prof. Dr. Marin", "faculty_id": 21, "year": 1, "semester": 1},
            {"name": "Anatomia descriptiva si functionala a articulatiilor membrului inferior: Articulatiile tibiofibuloasa proximala si distala, articulatia talocrurorala, articulatiile piciorului", "profesor_name": "Prof. Dr. Florescu", "faculty_id": 21, "year": 1, "semester": 1},
            
            # From image 2
            {"name": "Dezvoltarea sistemului respirator. Morfogeneza sistemului respirator inferior (traheo-bronho-pneumo-alveolara). Maturarea planmonilor", "profesor_name": "Prof. Dr. Neagu", "faculty_id": 21, "year": 1, "semester": 2},
            {"name": "Principii de organizare a sistemului respirator. Subsisteme de ventilatie, perfuzie si difuziune. Organizarea functionala a mediastinului. Anatomia clinica", "profesor_name": "Prof. Dr. Dragomir", "faculty_id": 21, "year": 1, "semester": 2},
            {"name": "Dezvoltarea cordului. Localizarea ariei cardiogene. Formarea tubului si ansei cardiace. Dezvoltarea septelor cordului. Formarea sistemului vascular arterial si venos", "profesor_name": "Prof. Dr. Stanescu", "faculty_id": 21, "year": 1, "semester": 2},
            {"name": "Dezvoltarea sistemului vascular. Circulatia fetala si neonatala. Principiu de organizare functionala a cordului si vaselor", "profesor_name": "Prof. Dr. Dumitrescu", "faculty_id": 21, "year": 1, "semester": 2}
        ]
        
        # Add courses to database
        courses_added = 0
        print("Adding Medicina courses to the database...")
        print("-" * 80)
        
        for course_data in medicina_courses:
            # Check if course already exists
            existing_course = db.query(Course).filter(Course.name == course_data["name"]).first()
            if existing_course:
                print(f"Course already exists: {course_data['name'][:50]}...")
            else:
                new_course = Course(**course_data)
                db.add(new_course)
                courses_added += 1
                print(f"Added: {course_data['name'][:50]}...")
        
        # Commit changes
        db.commit()
        print("-" * 80)
        print(f"Added {courses_added} new Medicina courses to the database")
        
        # List all Medicina courses
        medicina_courses = db.query(Course).filter(
            Course.faculty_id == "21"
        ).all()
        
        print(f"\nMedicina courses in database ({len(medicina_courses)}):")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<70} {'Professor':<20}")
        print("-" * 80)
        
        for course in medicina_courses:
            print(f"{course.id:<5} {course.name[:70]}... {course.profesor_name:<20}")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"Error adding Medicina courses: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_medicina_courses()
