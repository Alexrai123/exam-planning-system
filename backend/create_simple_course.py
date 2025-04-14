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

def create_simple_course():
    """Create a simple course that will definitely work"""
    print("Creating a simple test course...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Define the test professor and course
    test_professor_name = "Simple Test Professor"
    test_course_name = "Simple Test Course"
    
    # Check if the professor already exists
    cursor.execute("SELECT name FROM professors WHERE name = %s", (test_professor_name,))
    professor = cursor.fetchone()
    
    if not professor:
        print(f"Creating test professor: {test_professor_name}")
        cursor.execute("""
            INSERT INTO professors (name, specialization, title, email, phone, faculty)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (test_professor_name, "Computer Science", "PhD", "simple.test@example.com", "123456789", "Test Faculty"))
    else:
        print(f"Professor {test_professor_name} already exists")
    
    # Check if the course already exists
    cursor.execute("SELECT id FROM courses WHERE name = %s", (test_course_name,))
    course = cursor.fetchone()
    
    if not course:
        print(f"Creating test course: {test_course_name}")
        cursor.execute("""
            INSERT INTO courses (name, profesor_name, credits, year, semester, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (test_course_name, test_professor_name, 5, 2, 1, "A simple test course"))
        
        course_id = cursor.fetchone()[0]
        print(f"Created test course with ID: {course_id}")
    else:
        print(f"Course {test_course_name} already exists with ID: {course[0]}")
    
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
    
    print("\nSimple course creation completed!")
    print("You can now create exams using the simple test course.")

if __name__ == "__main__":
    create_simple_course()
