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

def add_faculty_column():
    """
    Add faculty_id column to courses table
    """
    print("Adding faculty_id column to courses table...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the column already exists
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'courses' AND column_name = 'faculty_id'
    """)
    
    if cursor.fetchone() is None:
        # Add the faculty_id column
        cursor.execute("""
            ALTER TABLE courses 
            ADD COLUMN faculty_id VARCHAR(10) REFERENCES faculties(id)
        """)
        print("Column added successfully")
    else:
        print("Column already exists")
    
    # Update courses with faculty information
    print("Updating courses with faculty information...")
    cursor.execute("""
        UPDATE courses c
        SET faculty_id = f.id
        FROM professors p, faculties f
        WHERE c.profesor_name = p.name
        AND p.faculty = f.name
        AND c.faculty_id IS NULL
    """)
    courses_updated = cursor.rowcount
    print(f"Updated {courses_updated} courses with faculty information")
    
    conn.close()

if __name__ == "__main__":
    add_faculty_column()
