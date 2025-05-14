"""
Script to remove professors from courses
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def remove_course_professors():
    """
    Remove professors from courses
    """
    try:
        with engine.connect() as conn:
            # Check course table structure
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'courses' AND column_name = 'profesor_name'"
            ))
            
            if result.rowcount > 0:
                # Backup courses with professor names
                print("Creating backup of courses with professor names...")
                conn.execute(text(
                    "CREATE TABLE IF NOT EXISTS courses_backup AS SELECT * FROM courses"
                ))
                print("Backup created as courses_backup table")
                
                # Update courses to set profesor_name to NULL
                result = conn.execute(text(
                    "UPDATE courses SET profesor_name = NULL"
                ))
                
                print(f"Removed professor assignments from {result.rowcount} courses")
                
                # List updated courses
                result = conn.execute(text(
                    "SELECT id, name, profesor_name, faculty_id, year, semester FROM courses WHERE faculty_id = '21'"
                ))
                rows = result.fetchall()
                
                print(f"\nUpdated courses for FMSB (Faculty ID 21) in database ({len(rows)}):")
                print("-" * 80)
                print(f"{'ID':<5} {'Name':<30} {'Professor':<30} {'Year':<5} {'Semester':<5}")
                print("-" * 80)
                
                for row in rows:
                    prof = row[2] if row[2] else "None"
                    print(f"{row[0]:<5} {row[1]:<30} {prof:<30} {row[3]:<5} {row[4]:<5}")
                
                print("-" * 80)
            else:
                print("No profesor_name column found in courses table")
        
    except Exception as e:
        print(f"Error removing course professors: {e}")

if __name__ == "__main__":
    remove_course_professors()
