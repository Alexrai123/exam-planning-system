"""
Script to list all specializations in the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def list_specializations():
    """
    List all specializations in the database
    """
    try:
        with engine.connect() as conn:
            # Get all specializations
            result = conn.execute(text(
                """
                SELECT s.id, s.name, s.short_name, s.faculty_id, f.short_name as faculty_short_name
                FROM specializations s
                JOIN faculties f ON s.faculty_id = f.id
                ORDER BY f.short_name, s.name
                """
            ))
            specializations = result.fetchall()
            
            print(f"Total specializations in database: {len(specializations)}")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<60} {'Short Name':<15} {'Faculty ID':<12} {'Faculty':<10}")
            print("-" * 80)
            
            current_faculty = None
            for spec in specializations:
                if current_faculty != spec[4]:
                    current_faculty = spec[4]
                    print(f"\nSpecializations for faculty: {current_faculty}")
                    print("-" * 80)
                
                print(f"{spec[0]:<5} {spec[1][:60]:<60} {spec[2]:<15} {spec[3]:<12} {spec[4]:<10}")
            
            print("-" * 80)
            
            # Count specializations by faculty
            result = conn.execute(text(
                """
                SELECT f.id, f.short_name, COUNT(s.id) as spec_count
                FROM faculties f
                LEFT JOIN specializations s ON f.id = s.faculty_id
                GROUP BY f.id, f.short_name
                ORDER BY f.short_name
                """
            ))
            faculty_counts = result.fetchall()
            
            print(f"\nSpecialization counts by faculty:")
            print("-" * 80)
            print(f"{'Faculty ID':<12} {'Faculty':<15} {'Specialization Count':<20}")
            print("-" * 80)
            
            for row in faculty_counts:
                print(f"{row[0]:<12} {row[1]:<15} {row[2]:<20}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error listing specializations: {e}")

if __name__ == "__main__":
    list_specializations()
