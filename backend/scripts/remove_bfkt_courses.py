"""
Script to remove Balneofiziokinetoterapie si recuperare (BFKT) courses from the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def remove_bfkt_courses():
    """
    Remove Balneofiziokinetoterapie si recuperare (BFKT) courses from the database
    """
    try:
        with engine.connect() as conn:
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
            
            # Get list of BFKT courses to remove
            result = conn.execute(text(
                """
                SELECT id, name
                FROM courses 
                WHERE faculty_id = '21' 
                AND (
                    name LIKE 'Anatomie functionala%'
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
                    OR name LIKE 'Fiziologie%'
                    OR name LIKE 'Biofizica%'
                    OR name LIKE 'Psihologie%'
                    OR name LIKE 'Educatie%'
                )
                ORDER BY id
                """
            ))
            courses_to_remove = result.fetchall()
            
            print(f"\nFound {len(courses_to_remove)} BFKT courses to remove:")
            print("-" * 80)
            for course in courses_to_remove:
                print(f"ID: {course[0]}, Name: {course[1]}")
            print("-" * 80)
            
            # Confirm removal
            print(f"\nRemoving {len(courses_to_remove)} BFKT courses...")
            
            # Delete courses
            for course in courses_to_remove:
                conn.execute(text(
                    "DELETE FROM courses WHERE id = :id"
                ), {"id": course[0]})
                print(f"Removed course: {course[1]}")
            
            conn.commit()
            print("-" * 80)
            print(f"Successfully removed {len(courses_to_remove)} BFKT courses from the database")
            
            # Verify removal
            result = conn.execute(text(
                """
                SELECT COUNT(*) 
                FROM courses 
                WHERE faculty_id = '21' 
                AND (
                    name LIKE 'Anatomie functionala%'
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
                """
            ))
            remaining_count = result.scalar()
            
            if remaining_count == 0:
                print("Verification successful: All BFKT courses have been removed")
            else:
                print(f"Warning: {remaining_count} BFKT courses still remain in the database")
        
    except Exception as e:
        print(f"Error removing BFKT courses: {e}")

if __name__ == "__main__":
    remove_bfkt_courses()
