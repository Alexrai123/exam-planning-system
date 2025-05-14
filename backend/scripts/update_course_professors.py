"""
Script to update course professors to a placeholder value
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def update_course_professors():
    """
    Update course professors to a placeholder value
    """
    try:
        with engine.connect() as conn:
            # Set placeholder value for professor name
            placeholder = "N/A"
            
            # Update courses to set profesor_name to placeholder
            result = conn.execute(text(
                "UPDATE courses SET profesor_name = :placeholder"
            ), {"placeholder": placeholder})
            
            conn.commit()
            print(f"Updated professor assignments to '{placeholder}' for {result.rowcount} courses")
            
            # List updated courses
            result = conn.execute(text(
                "SELECT id, name, profesor_name, faculty_id, year, semester FROM courses WHERE faculty_id = '21'"
            ))
            rows = result.fetchall()
            
            print(f"\nUpdated courses for FMSB (Faculty ID 21) in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<30} {'Professor':<30} {'Faculty ID':<10} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<30} {row[2]:<30} {row[3]:<10} {row[4]:<5} {row[5]:<5}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error updating course professors: {e}")

if __name__ == "__main__":
    update_course_professors()
