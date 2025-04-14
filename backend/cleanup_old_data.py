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

def cleanup_data():
    """
    Clean up old test data that wasn't imported from the API
    """
    print("Starting data cleanup...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First, let's back up the courses and exams that might be deleted
    print("Backing up courses and exams before deletion...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses_backup AS
        SELECT * FROM courses
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams_backup AS
        SELECT * FROM exams
    """)
    
    # Get a list of professors from the API (these are the ones we want to keep)
    cursor.execute("""
        SELECT name FROM professors 
        WHERE email IS NOT NULL OR phone IS NOT NULL OR faculty IS NOT NULL
    """)
    api_professors = [row[0] for row in cursor.fetchall()]
    
    # Get a list of rooms from the API (these are the ones we want to keep)
    cursor.execute("""
        SELECT name FROM sala 
        WHERE building IS NOT NULL OR capacity IS NOT NULL OR computers IS NOT NULL
    """)
    api_rooms = [row[0] for row in cursor.fetchall()]
    
    # Get a list of groups from the API (these are the ones we want to keep)
    cursor.execute("""
        SELECT name FROM grupa 
        WHERE year IS NOT NULL OR specialization IS NOT NULL
    """)
    api_groups = [row[0] for row in cursor.fetchall()]
    
    # Get courses that reference non-API professors
    cursor.execute("""
        SELECT id FROM courses 
        WHERE profesor_name NOT IN %s
    """, (tuple(api_professors) if api_professors else ('',),))
    old_course_ids = [row[0] for row in cursor.fetchall()]
    
    # Delete exams that reference old courses
    print("Deleting exams that reference old courses...")
    if old_course_ids:
        cursor.execute("""
            DELETE FROM exams 
            WHERE course_id IN %s
        """, (tuple(old_course_ids),))
        exams_deleted_courses = cursor.rowcount
    else:
        exams_deleted_courses = 0
    
    # Delete exams that reference non-API rooms or groups
    print("Deleting exams that reference old rooms or groups...")
    cursor.execute("""
        DELETE FROM exams 
        WHERE sala_name NOT IN %s OR grupa_name NOT IN %s
    """, (tuple(api_rooms) if api_rooms else ('',), tuple(api_groups) if api_groups else ('',)))
    exams_deleted_rooms_groups = cursor.rowcount
    
    # Now we can safely delete courses that reference non-API professors
    print("Deleting courses that reference old professors...")
    cursor.execute("""
        DELETE FROM courses 
        WHERE profesor_name NOT IN %s
    """, (tuple(api_professors) if api_professors else ('',),))
    courses_deleted = cursor.rowcount
    
    # Delete professors that aren't from the API
    print("Deleting old professors...")
    cursor.execute("""
        DELETE FROM professors 
        WHERE name NOT IN %s
    """, (tuple(api_professors) if api_professors else ('',),))
    professors_deleted = cursor.rowcount
    
    # Delete rooms that aren't from the API
    print("Deleting old rooms...")
    cursor.execute("""
        DELETE FROM sala 
        WHERE name NOT IN %s
    """, (tuple(api_rooms) if api_rooms else ('',),))
    rooms_deleted = cursor.rowcount
    
    # Delete groups that aren't from the API
    print("Deleting old groups...")
    cursor.execute("""
        DELETE FROM grupa 
        WHERE name NOT IN %s
    """, (tuple(api_groups) if api_groups else ('',),))
    groups_deleted = cursor.rowcount
    
    # Get faculties for mapping professors to faculties
    cursor.execute("SELECT id, name FROM faculties")
    faculties = {row[1]: row[0] for row in cursor.fetchall()}
    
    # Update courses to include faculty_id based on professor's faculty
    print("Updating courses with faculty information...")
    cursor.execute("""
        UPDATE courses c
        SET faculty_id = f.id
        FROM professors p, faculties f
        WHERE c.profesor_name = p.name
        AND p.faculty = f.name
        AND c.faculty_id IS NULL
    """)
    courses_updated_faculty = cursor.rowcount
    
    # Create sample courses for each professor if they don't have any
    print("Creating sample courses for professors without courses...")
    cursor.execute("""
        SELECT p.name, p.faculty
        FROM professors p
        LEFT JOIN courses c ON p.name = c.profesor_name
        WHERE c.id IS NULL
        LIMIT 50
    """)
    professors_without_courses = cursor.fetchall()
    
    courses_created = 0
    for i, (professor_name, faculty_name) in enumerate(professors_without_courses):
        # Get professor's specialization
        cursor.execute("SELECT specialization FROM professors WHERE name = %s", (professor_name,))
        specialization_row = cursor.fetchone()
        specialization = specialization_row[0] if specialization_row and specialization_row[0] else "General"
        
        # Get faculty_id if available
        faculty_id = faculties.get(faculty_name)
        
        # Create a sample course for this professor
        course_name = f"Course in {specialization} {i+1}"
        cursor.execute("""
            INSERT INTO courses (name, profesor_name, faculty_id, credits, year, semester, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (course_name, professor_name, faculty_id, 5, 2, 1, f"A course in {specialization} taught by {professor_name}"))
        courses_created += 1
    
    conn.close()
    
    print("\nCleanup completed!")
    print(f"Exams deleted (old courses): {exams_deleted_courses}")
    print(f"Exams deleted (old rooms/groups): {exams_deleted_rooms_groups}")
    print(f"Courses deleted: {courses_deleted}")
    print(f"Professors deleted: {professors_deleted}")
    print(f"Rooms deleted: {rooms_deleted}")
    print(f"Groups deleted: {groups_deleted}")
    print(f"Courses updated with faculty: {courses_updated_faculty}")
    print(f"Sample courses created: {courses_created}")

if __name__ == "__main__":
    cleanup_data()
