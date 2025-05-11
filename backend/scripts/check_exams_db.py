"""
Script to check the exam status and professor agreement values in the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import get_db
from sqlalchemy import text

def check_exams_database():
    """Check the exam status and professor agreement values in the database"""
    db = next(get_db())
    try:
        # Use raw SQL to query the database
        query = text("""
            SELECT id, status, professor_agreement 
            FROM exams 
            ORDER BY id
        """)
        
        results = db.execute(query).fetchall()
        
        print("Exam records in the database:")
        print("ID | Status | Professor Agreement")
        print("-" * 40)
        
        for row in results:
            exam_id = row[0]
            status = row[1]
            professor_agreement = row[2]
            print(f"{exam_id} | {status} | {professor_agreement}")
        
        # Now let's update all confirmed exams to have professor_agreement = TRUE
        update_query = text("""
            UPDATE exams 
            SET professor_agreement = TRUE 
            WHERE status = 'CONFIRMED' AND professor_agreement = FALSE
        """)
        
        result = db.execute(update_query)
        db.commit()
        
        affected_rows = result.rowcount
        print(f"\nUpdated {affected_rows} confirmed exams to have professor_agreement = TRUE")
        
        # Check again after update
        results = db.execute(query).fetchall()
        
        print("\nExam records after update:")
        print("ID | Status | Professor Agreement")
        print("-" * 40)
        
        for row in results:
            exam_id = row[0]
            status = row[1]
            professor_agreement = row[2]
            print(f"{exam_id} | {status} | {professor_agreement}")
        
    except Exception as e:
        print(f"Error checking database: {e}")
        db.rollback()

if __name__ == "__main__":
    check_exams_database()
