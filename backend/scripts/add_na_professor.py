"""
Script to add an N/A professor and update courses
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_na_professor():
    """
    Add an N/A professor and update courses
    """
    try:
        with engine.connect() as conn:
            # Add N/A professor if it doesn't exist
            placeholder = "N/A"
            
            # Check if N/A professor exists
            result = conn.execute(text(
                "SELECT name FROM professors WHERE name = :name"
            ), {"name": placeholder})
            
            if result.rowcount == 0:
                # Create N/A professor
                conn.execute(text(
                    "INSERT INTO professors (name, faculty) VALUES (:name, 'N/A')"
                ), {"name": placeholder})
                
                conn.commit()
                print(f"Created placeholder professor: {placeholder}")
            else:
                print(f"Placeholder professor '{placeholder}' already exists")
            
            # Update courses to use N/A professor
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
        print(f"Error updating professors: {e}")

if __name__ == "__main__":
    add_na_professor()
