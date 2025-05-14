"""
Script to list all faculties in the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def list_all_faculties():
    """
    List all faculties in the database
    """
    try:
        with engine.connect() as conn:
            # Check if faculties table exists
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_name = 'faculties'"
            ))
            if result.rowcount == 0:
                print("Faculties table not found in the database.")
                return
            
            # Get columns from faculties table
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'faculties'"
            ))
            columns = [row[0] for row in result]
            print(f"Columns in faculties table: {', '.join(columns)}")
            
            # Query faculties table
            query = "SELECT id, name"
            if "abbreviation" in columns:
                query += ", abbreviation"
            else:
                query += ", NULL as abbreviation"
            query += " FROM faculties"
            
            result = conn.execute(text(query))
            rows = result.fetchall()
            
            print(f"\nFound {len(rows)} faculties in the database:")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Abbreviation':<15}")
            print("-" * 80)
            for row in rows:
                try:
                    faculty_id = str(row[0])
                    faculty_name = str(row[1]) if row[1] else 'N/A'
                    abbr = str(row[2]) if len(row) > 2 and row[2] else 'N/A'
                    print(f"{faculty_id:<5} {faculty_name:<50} {abbr:<15}")
                except UnicodeEncodeError:
                    # Handle encoding issues by printing ID only
                    print(f"{row[0]:<5} <Name contains special characters> {abbr:<15}")
            print("-" * 80)
    except Exception as e:
        print(f"Error listing faculties: {e}")

if __name__ == "__main__":
    list_all_faculties()
