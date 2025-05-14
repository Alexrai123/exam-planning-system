"""
Script to list all faculties in the database using a simpler approach
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import get_db
from app.models.faculty import Faculty

def list_all_faculties():
    """
    List all faculties in the database using ORM
    """
    try:
        db = next(get_db())
        faculties = db.query(Faculty).all()
        
        print(f"Found {len(faculties)} faculties in the database:")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<50} {'Short Name':<15}")
        print("-" * 80)
        
        for faculty in faculties:
            try:
                faculty_id = str(faculty.id)
                faculty_name = faculty.name if faculty.name else 'N/A'
                short_name = faculty.short_name if hasattr(faculty, 'short_name') and faculty.short_name else 'N/A'
                
                print(f"{faculty_id:<5} {faculty_name:<50} {short_name:<15}")
            except Exception as e:
                print(f"{faculty.id:<5} <Display error: {str(e)[:30]}...>")
        
        print("-" * 80)
    except Exception as e:
        print(f"Error listing faculties: {e}")

if __name__ == "__main__":
    list_all_faculties()
