"""
Script to clean test data from the database while preserving important data
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db

def clean_test_data():
    """
    Clean test data from the database
    """
    db = next(get_db())
    try:
        print("Cleaning test data from the database...")
        
        # Remove test professors
        test_professors = ["Simple Test Professor", "None None", "John Smith"]
        for professor in test_professors:
            # Escape single quotes for SQL
            escaped_name = professor.replace("'", "''")
            delete_query = text(f"DELETE FROM professors WHERE name = '{escaped_name}'")
            result = db.execute(delete_query)
            if result.rowcount > 0:
                print(f"Deleted test professor: {professor}")
            else:
                print(f"Professor not found: {professor}")
        
        # Commit changes
        db.commit()
        print("Test data cleaned successfully!")
        
    except Exception as e:
        print(f"Error cleaning test data: {e}")
        db.rollback()

def check_database_content():
    """
    Check the current content of the database
    """
    db = next(get_db())
    try:
        # Check professors
        professors_query = text("SELECT COUNT(*) FROM professors")
        professors_count = db.execute(professors_query).scalar()
        print(f"Current professors count: {professors_count}")

        # Check rooms
        rooms_query = text("SELECT COUNT(*) FROM sala")
        rooms_count = db.execute(rooms_query).scalar()
        print(f"Current rooms count: {rooms_count}")

        # Check groups
        groups_query = text("SELECT COUNT(*) FROM grupa")
        groups_count = db.execute(groups_query).scalar()
        print(f"Current groups count: {groups_count}")

        # Check faculties
        faculties_query = text("SELECT COUNT(*) FROM faculties")
        faculties_count = db.execute(faculties_query).scalar()
        print(f"Current faculties count: {faculties_count}")

        # Check courses
        courses_query = text("SELECT COUNT(*) FROM courses")
        courses_count = db.execute(courses_query).scalar()
        print(f"Current courses count: {courses_count}")

        # Check exams
        exams_query = text("SELECT COUNT(*) FROM exams")
        exams_count = db.execute(exams_query).scalar()
        print(f"Current exams count: {exams_count}")
        
    except Exception as e:
        print(f"Error checking database content: {e}")

if __name__ == "__main__":
    print("Checking current database content...")
    check_database_content()
    
    # Clean test data
    clean_test_data()
    
    # Check database content after cleaning
    print("\nDatabase content after cleaning:")
    check_database_content()
