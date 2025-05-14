"""
Script to get PostgreSQL database information for creating exams
"""
from app.db.base import get_db
from sqlalchemy import text

def main():
    # Get database connection
    db = next(get_db())
    
    # Check available tables
    print("AVAILABLE TABLES:")
    tables_query = text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = db.execute(tables_query).fetchall()
    for table in tables:
        print(f"- {table[0]}")
    print("\n")
    
    # Check column names for each table
    for table_name in ['sala', 'grupa', 'courses', 'exams']:
        print(f"COLUMNS IN {table_name.upper()} TABLE:")
        columns_query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = db.execute(columns_query).fetchall()
        for column in columns:
            print(f"- {column[0]}")
        print("\n")
    
    # Get courses
    print("AVAILABLE COURSES:")
    courses_query = text("SELECT id, name, profesor_name FROM courses LIMIT 10")
    courses = db.execute(courses_query).fetchall()
    for course in courses:
        print(f"ID: {course[0]}, Name: {course[1]}, Professor: {course[2]}")
    print("\n")
    
    # Get rooms (sala table)
    print("AVAILABLE ROOMS:")
    rooms_query = text("SELECT name, capacity FROM sala LIMIT 10")
    rooms = db.execute(rooms_query).fetchall()
    for room in rooms:
        print(f"Name: {room[0]}, Capacity: {room[1]}")
    print("\n")
    
    # Get groups (grupa table)
    print("AVAILABLE GROUPS:")
    groups_query = text("SELECT name, year, specialization FROM grupa LIMIT 10")
    groups = db.execute(groups_query).fetchall()
    for group in groups:
        print(f"Name: {group[0]}, Year: {group[1]}, Specialization: {group[2]}")
    print("\n")
    
    # Get existing exams
    print("EXISTING EXAMS:")
    exams_query = text("SELECT id, course_id, date, sala_name, grupa_name, status FROM exams LIMIT 10")
    exams = db.execute(exams_query).fetchall()
    for exam in exams:
        print(f"ID: {exam[0]}, Course ID: {exam[1]}, Date: {exam[2]}, Room: {exam[3]}, Group: {exam[4]}, Status: {exam[5]}")
    print("\n")

if __name__ == "__main__":
    main()
