"""
Script to list all Medicina courses in the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def list_medicina_courses():
    """
    List all Medicina courses in the database
    """
    try:
        with engine.connect() as conn:
            # Get specialization ID for Medicina
            result = conn.execute(text(
                "SELECT id FROM specializations WHERE name = 'Medicina'"
            ))
            med_spec_id = result.scalar()
            
            if med_spec_id:
                print(f"Found Medicina specialization with ID: {med_spec_id}")
            
            # List all courses for FMSB (Faculty ID 21)
            result = conn.execute(text(
                "SELECT id, name, year, semester FROM courses WHERE faculty_id = '21' ORDER BY id"
            ))
            rows = result.fetchall()
            
            print(f"\nAll Medicina courses in database ({len(rows)}):")
            print("-" * 100)
            print(f"{'ID':<5} {'Name':<80} {'Year':<5} {'Semester':<5}")
            print("-" * 100)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<80} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 100)
        
    except Exception as e:
        print(f"Error listing Medicina courses: {e}")

if __name__ == "__main__":
    list_medicina_courses()
