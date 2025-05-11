"""
Script to inspect and update all confirmed exams to have professor_agreement set to True
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import in the correct order to avoid circular imports
from app.db.base import get_db
from sqlalchemy import text

def inspect_and_update_exams():
    """Inspect the database and update confirmed exams"""
    db = next(get_db())
    try:
        # First, inspect the exams table to see how status is stored
        inspect_sql = text("SELECT id, status::text, professor_agreement FROM exams LIMIT 10")
        results = db.execute(inspect_sql).fetchall()
        
        print("Sample exam records:")
        for row in results:
            print(f"ID: {row[0]}, Status: {row[1]}, Professor Agreement: {row[2]}")
        
        # Now get all confirmed exams where professor_agreement is False
        confirmed_status_values = ['confirmed', 'CONFIRMED', 'ExamStatus.CONFIRMED']
        
        for status_value in confirmed_status_values:
            try:
                # Try to update with this status value
                update_sql = text(f"""
                    UPDATE exams 
                    SET professor_agreement = TRUE 
                    WHERE status::text LIKE '%{status_value}%' AND professor_agreement = FALSE
                """)
                
                result = db.execute(update_sql)
                db.commit()
                
                count = result.rowcount
                if count > 0:
                    print(f"Updated {count} exams with status containing '{status_value}'.")
            except Exception as e:
                print(f"Error with status value '{status_value}': {e}")
                db.rollback()
        
        print("Update operation completed.")
        
    except Exception as e:
        print(f"Error inspecting/updating exams: {e}")
        db.rollback()

if __name__ == "__main__":
    inspect_and_update_exams()
