"""
Script to check the database schema
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db

def check_schema():
    """Check the database schema"""
    db = next(get_db())
    try:
        # Check professors table schema
        professors_schema = text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'professors'
        """)
        professors_columns = db.execute(professors_schema).fetchall()
        print("\nProfessors table schema:")
        for column in professors_columns:
            print(f"  {column[0]} ({column[1]})")
        
        # Check rooms table schema
        rooms_schema = text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'sala'
        """)
        rooms_columns = db.execute(rooms_schema).fetchall()
        print("\nRooms table schema:")
        for column in rooms_columns:
            print(f"  {column[0]} ({column[1]})")
        
        # Check groups table schema
        groups_schema = text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'grupa'
        """)
        groups_columns = db.execute(groups_schema).fetchall()
        print("\nGroups table schema:")
        for column in groups_columns:
            print(f"  {column[0]} ({column[1]})")
        
        # Check faculties table schema
        faculties_schema = text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'faculties'
        """)
        faculties_columns = db.execute(faculties_schema).fetchall()
        print("\nFaculties table schema:")
        for column in faculties_columns:
            print(f"  {column[0]} ({column[1]})")
        
    except Exception as e:
        print(f"Error checking schema: {e}")

if __name__ == "__main__":
    check_schema()
