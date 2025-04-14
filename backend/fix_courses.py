import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("POSTGRES_HOST", "exam_planning_db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "exam_planning")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    return conn

def fix_courses():
    """Fix issues with courses in the database"""
    print("Checking and fixing courses...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check for NULL profesor_name in courses
    cursor.execute("SELECT id, name FROM courses WHERE profesor_name IS NULL")
    null_professor_courses = cursor.fetchall()
    
    if null_professor_courses:
        print(f"Found {len(null_professor_courses)} courses with NULL professor_name:")
        for course in null_professor_courses:
            print(f"ID: {course[0]}, Name: {course[1]}")
        
        # Get a valid professor name to use
        cursor.execute("SELECT name FROM professors WHERE name IS NOT NULL LIMIT 1")
        valid_professor = cursor.fetchone()[0]
        
        # Update courses with NULL professor_name
        cursor.execute("""
            UPDATE courses
            SET profesor_name = %s
            WHERE profesor_name IS NULL
        """, (valid_professor,))
        
        print(f"Updated {cursor.rowcount} courses with professor: {valid_professor}")
    else:
        print("No courses with NULL professor_name found.")
    
    # Create a simple test course that should definitely work
    cursor.execute("""
        INSERT INTO courses (name, profesor_name, credits, year, semester, description)
        VALUES ('Simple Test Course', 'Test Professor', 5, 2, 1, 'A simple test course')
        ON CONFLICT (id) DO NOTHING
        RETURNING id
    """)
    
    result = cursor.fetchone()
    if result:
        print(f"Created simple test course with ID: {result[0]}")
    else:
        print("Simple test course already exists or couldn't be created")
    
    # Print all courses for verification
    cursor.execute("""
        SELECT id, name, profesor_name
        FROM courses
        ORDER BY id DESC
        LIMIT 10
    """)
    
    courses = cursor.fetchall()
    print(f"\nLatest 10 courses in the database:")
    for course in courses:
        print(f"ID: {course[0]}, Name: {course[1]}, Professor: {course[2]}")
    
    conn.close()
    
    print("\nCourse fixes completed!")

if __name__ == "__main__":
    fix_courses()
