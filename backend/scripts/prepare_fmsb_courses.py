"""
Script to prepare for adding FMSB courses to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import get_db
from app.models.faculty import Faculty

def prepare_fmsb_courses():
    """
    Prepare for adding FMSB courses by listing programs/specializations
    """
    try:
        db = next(get_db())
        
        # Check if FMSB faculty exists
        fmsb = db.query(Faculty).filter(Faculty.id == "21").first()
        if not fmsb:
            print("FMSB faculty not found in the database.")
            return
        
        print(f"Faculty: {fmsb.name} (ID: {fmsb.id}, Short Name: {fmsb.short_name})")
        
        # List FMSB programs/specializations
        programs = [
            "Medicina",
            "Asistenta medicala generala",
            "Balneofiziokinetoterapie și recuperare",
            "Biochimie",
            "Biologie",
            "Nutritie si dietetica",
            "Tehnica dentara",
            "Master – Nutriție și Recuperare Medicală"
        ]
        
        print("\nFMSB Programs/Specializations:")
        print("-" * 80)
        for i, program in enumerate(programs, 1):
            print(f"{i}. {program}")
        print("-" * 80)
        
        # Suggest approach for adding courses
        print("\nSuggested approach for adding courses:")
        print("1. Use the existing structure: Add courses with faculty_id = 21 (FMSB)")
        print("   - Include the program/specialization in the course name or description")
        print("   - Example: 'Medicina - Anatomie' for a course in the Medicine program")
        print("\n2. Add a program/specialization field to the Course model:")
        print("   - This would require modifying the database schema")
        print("   - Example: Add a 'program' column to the 'courses' table")
        print("\nNote: Option 1 is simpler and doesn't require schema changes.")
        
    except Exception as e:
        print(f"Error preparing FMSB courses: {e}")

if __name__ == "__main__":
    prepare_fmsb_courses()
