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

def add_test_course():
    """Add a test course to the database"""
    print("Adding a test course...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First, check if we have any professors in the database
    cursor.execute("SELECT name FROM professors LIMIT 1")
    professor = cursor.fetchone()
    
    if not professor:
        print("No professors found in the database. Creating a test professor...")
        cursor.execute("""
            INSERT INTO professors (name, specialization, title, email, phone, faculty)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING name
        """, ("Test Professor", "Computer Science", "PhD", "test.professor@example.com", "123456789", "Faculty of Computer Science"))
        professor_name = cursor.fetchone()[0]
        print(f"Created test professor: {professor_name}")
    else:
        professor_name = professor[0]
        print(f"Using existing professor: {professor_name}")
    
    # Check if we have any faculties
    cursor.execute("SELECT id, name FROM faculties LIMIT 1")
    faculty = cursor.fetchone()
    
    faculty_id = None
    if faculty:
        faculty_id = faculty[0]
        print(f"Using existing faculty: {faculty[1]} (ID: {faculty_id})")
    
    # Check if the test course already exists
    cursor.execute("SELECT id FROM courses WHERE name = %s", ("Test Course",))
    existing_course = cursor.fetchone()
    
    if existing_course:
        print(f"Test course already exists with ID: {existing_course[0]}")
        course_id = existing_course[0]
    else:
        # Create a new test course
        cursor.execute("""
            INSERT INTO courses (name, profesor_name, faculty_id, credits, year, semester, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ("Test Course", professor_name, faculty_id, 5, 2, 1, "A test course for creating exams"))
        
        course_id = cursor.fetchone()[0]
        print(f"Created new test course with ID: {course_id}")
    
    # Print all courses for verification
    cursor.execute("""
        SELECT c.id, c.name, c.profesor_name, f.name as faculty_name
        FROM courses c
        LEFT JOIN faculties f ON c.faculty_id = f.id
        ORDER BY c.id
    """)
    
    courses = cursor.fetchall()
    print(f"\nAll courses in the database ({len(courses)}):")
    for course in courses:
        print(f"ID: {course[0]}, Name: {course[1]}, Professor: {course[2]}, Faculty: {course[3] or 'None'}")
    
    conn.close()
    
    print("\nTest course creation completed!")
    print("You can now create exams using the test course.")

if __name__ == "__main__":
    add_test_course()
