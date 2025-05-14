"""
Script to update Medicina course semesters
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def update_medicina_semesters():
    """
    Update Medicina course semesters to have first half in semester 1 and second half in semester 2
    """
    try:
        with engine.connect() as conn:
            # Update courses C1-C7 to semester 1
            result = conn.execute(text(
                """
                UPDATE courses 
                SET semester = 1
                WHERE name LIKE 'C_. %' AND CAST(SUBSTRING(name, 2, 1) AS INTEGER) <= 7
                """
            ))
            print(f"Updated {result.rowcount} courses to semester 1")
            
            # Update courses C8-C14 to semester 2
            result = conn.execute(text(
                """
                UPDATE courses 
                SET semester = 2
                WHERE name LIKE 'C_. %' AND CAST(SUBSTRING(name, 2, 1) AS INTEGER) > 7
                """
            ))
            print(f"Updated {result.rowcount} courses to semester 2")
            
            # Update courses C10-C14 to semester 2 (for two-digit course numbers)
            result = conn.execute(text(
                """
                UPDATE courses 
                SET semester = 2
                WHERE name LIKE 'C__. %'
                """
            ))
            print(f"Updated {result.rowcount} additional courses to semester 2")
            
            conn.commit()
            
            # List all Medicina courses
            result = conn.execute(text(
                "SELECT id, name, year, semester FROM courses WHERE faculty_id = '21' ORDER BY year, semester, name"
            ))
            rows = result.fetchall()
            
            print(f"\nUpdated Medicina courses in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Year':<5} {'Semester':<5}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<50} {row[2]:<5} {row[3]:<5}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error updating Medicina course semesters: {e}")

if __name__ == "__main__":
    update_medicina_semesters()
