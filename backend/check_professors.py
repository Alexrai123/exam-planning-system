"""
Script to check professors table structure and data
"""
from app.db.base import get_db
from sqlalchemy import text

def main():
    # Get database connection
    db = next(get_db())
    
    # Check professors table columns
    print("PROFESSORS TABLE COLUMNS:")
    columns_query = text("SELECT column_name FROM information_schema.columns WHERE table_name = 'professors'")
    columns = db.execute(columns_query).fetchall()
    for column in columns:
        print(f"- {column[0]}")
    
    # Check professors data
    print("\nPROFESSORS DATA:")
    professors_query = text("SELECT * FROM professors LIMIT 10")
    professors = db.execute(professors_query).fetchall()
    for professor in professors:
        print(professor)
    
    # Check courses with professor names
    print("\nCOURSES WITH PROFESSOR NAMES:")
    courses_query = text("SELECT id, name, profesor_name FROM courses WHERE profesor_name IS NOT NULL LIMIT 10")
    courses = db.execute(courses_query).fetchall()
    for course in courses:
        print(f"ID: {course[0]}, Course: {course[1]}, Professor: {course[2]}")

if __name__ == "__main__":
    main()
