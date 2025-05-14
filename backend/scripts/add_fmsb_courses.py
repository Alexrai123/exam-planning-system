"""
Script to add courses for FMSB faculty to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.course import Course

def add_fmsb_courses():
    """
    Add courses for FMSB faculty to the database
    """
    db = next(get_db())
    try:
        # Define FMSB courses by program/specialization
        fmsb_courses = {
            "Medicina": [
                {"name": "Medicina - Anatomie", "profesor_name": "Prof. Dr. Ionescu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "Medicina - Fiziologie", "profesor_name": "Prof. Dr. Popescu", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "Medicina - Biochimie", "profesor_name": "Prof. Dr. Georgescu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "Medicina - Histologie", "profesor_name": "Prof. Dr. Mihai", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "Medicina - Embriologie", "profesor_name": "Prof. Dr. Stoica", "faculty_id": 21, "year": 1, "semester": 1}
            ],
            "Asistenta medicala generala": [
                {"name": "AMG - Nursing General", "profesor_name": "Dr. Marinescu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "AMG - Anatomie", "profesor_name": "Dr. Vasilescu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "AMG - Fiziologie", "profesor_name": "Dr. Popa", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "AMG - Farmacologie", "profesor_name": "Dr. Dinu", "faculty_id": 21, "year": 2, "semester": 1}
            ],
            "Balneofiziokinetoterapie si recuperare": [
                {"name": "BFKT - Anatomie functionala", "profesor_name": "Dr. Radulescu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "BFKT - Kinetoterapie", "profesor_name": "Dr. Stancu", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "BFKT - Electroterapie", "profesor_name": "Dr. Marin", "faculty_id": 21, "year": 2, "semester": 1}
            ],
            "Biochimie": [
                {"name": "Biochimie - Chimie organica", "profesor_name": "Prof. Dr. Florescu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "Biochimie - Biochimie structurala", "profesor_name": "Prof. Dr. Neagu", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "Biochimie - Enzimologie", "profesor_name": "Prof. Dr. Dragomir", "faculty_id": 21, "year": 2, "semester": 1}
            ],
            "Biologie": [
                {"name": "Biologie - Biologie Celulara", "profesor_name": "Prof. Dr. Stanescu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "Biologie - Genetica", "profesor_name": "Prof. Dr. Dumitrescu", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "Biologie - Microbiologie", "profesor_name": "Prof. Dr. Barbu", "faculty_id": 21, "year": 2, "semester": 1}
            ],
            "Nutritie si dietetica": [
                {"name": "ND - Biochimia alimentatiei", "profesor_name": "Dr. Cojocaru", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "ND - Nutritie umana", "profesor_name": "Dr. Manole", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "ND - Dietetica", "profesor_name": "Dr. Iancu", "faculty_id": 21, "year": 2, "semester": 1}
            ],
            "Tehnica dentara": [
                {"name": "TD - Materiale dentare", "profesor_name": "Dr. Badea", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "TD - Morfologia dintilor", "profesor_name": "Dr. Olteanu", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "TD - Proteze dentare", "profesor_name": "Dr. Nistor", "faculty_id": 21, "year": 2, "semester": 1}
            ],
            "Master - Nutritie si Recuperare Medicala": [
                {"name": "Master NRM - Nutritie clinica avansata", "profesor_name": "Prof. Dr. Dobre", "faculty_id": 21, "year": 1, "semester": 1},
                {"name": "Master NRM - Recuperare medicala", "profesor_name": "Prof. Dr. Sandu", "faculty_id": 21, "year": 1, "semester": 2},
                {"name": "Master NRM - Cercetare stiintifica", "profesor_name": "Prof. Dr. Preda", "faculty_id": 21, "year": 1, "semester": 2}
            ]
        }
        
        # Add courses to database
        courses_added = 0
        print("Adding FMSB courses to the database...")
        
        for program, courses in fmsb_courses.items():
            print(f"\nProgram: {program}")
            print("-" * 80)
            
            for course_data in courses:
                # Check if course already exists
                existing_course = db.query(Course).filter(Course.name == course_data["name"]).first()
                if existing_course:
                    print(f"Course '{course_data['name']}' already exists")
                else:
                    new_course = Course(**course_data)
                    db.add(new_course)
                    courses_added += 1
                    print(f"Added: {course_data['name']} (Professor: {course_data['profesor_name']}, Year: {course_data['year']}, Semester: {course_data['semester']})")
        
        # Commit changes
        db.commit()
        print(f"\nAdded {courses_added} new FMSB courses to the database")
        
    except Exception as e:
        print(f"Error adding FMSB courses: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_fmsb_courses()
