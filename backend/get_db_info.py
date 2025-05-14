"""
Script to get database information for creating exams
"""
from app.db.base import get_db
from sqlalchemy import text

def main():
    # Get database connection
    db = next(get_db())
    
    # Check available tables
    print("AVAILABLE TABLES:")
    tables_query = text("SELECT name FROM sqlite_master WHERE type='table'")
    tables = db.execute(tables_query).fetchall()
    for table in tables:
        print(f"- {table[0]}")
    print("\n")
    
    # Get courses
    print("AVAILABLE COURSES:")
    courses_query = text("SELECT id, name, profesor_name FROM courses LIMIT 10")
    courses = db.execute(courses_query).fetchall()
    for course in courses:
        print(f"ID: {course[0]}, Name: {course[1]}, Professor: {course[2]}")
    print("\n")
    
    # Get rooms
    print("AVAILABLE ROOMS:")
    rooms_query = text("SELECT id, name, capacity FROM rooms LIMIT 10")
    rooms = db.execute(rooms_query).fetchall()
    for room in rooms:
        print(f"ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
    print("\n")
    
    # Get groups
    print("AVAILABLE GROUPS:")
    groups_query = text("SELECT id, name FROM groups LIMIT 10")
    groups = db.execute(groups_query).fetchall()
    for group in groups:
        print(f"ID: {group[0]}, Name: {group[1]}")
    print("\n")

if __name__ == "__main__":
    main()
