import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Database connection parameters for Docker environment
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "exam_planning_db"  # Use the Docker container name as the host
DB_PORT = "5432"
DB_NAME = "exam_planning"

# Create database connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def create_professor_course():
    """Create a test course for Professor John Smith and an exam for that course."""
    with engine.connect() as connection:
        # Begin transaction
        trans = connection.begin()
        try:
            # First, check if John Smith exists in the professors table
            check_professor_query = text("""
                SELECT name FROM professors WHERE name = :name
            """)
            
            professor_result = connection.execute(check_professor_query, {"name": "John Smith"})
            professor = professor_result.fetchone()
            
            if not professor:
                print("Professor John Smith not found in the professors table. Creating...")
                # Insert John Smith into professors table if not exists
                insert_professor_query = text("""
                    INSERT INTO professors (name, specialization)
                    VALUES (:name, :specialization)
                    ON CONFLICT (name) DO NOTHING
                    RETURNING name
                """)
                
                connection.execute(insert_professor_query, {
                    "name": "John Smith",
                    "specialization": "Computer Science"
                })
            
            # Create a test course for John Smith
            insert_course_query = text("""
                INSERT INTO courses (name, profesor_name, year, semester, credits, description)
                VALUES (:name, :profesor_name, :year, :semester, :credits, :description)
                ON CONFLICT (id) DO UPDATE 
                SET name = EXCLUDED.name, 
                    profesor_name = EXCLUDED.profesor_name
                RETURNING id, name
            """)
            
            course_result = connection.execute(insert_course_query, {
                "name": "Introduction to Programming - John Smith",
                "profesor_name": "John Smith",
                "year": 1,
                "semester": 1,
                "credits": 6,
                "description": "A test course for Professor John Smith"
            })
            
            course = course_result.fetchone()
            course_id = course[0]
            course_name = course[1]
            
            print(f"Created/Updated course: {course_name} (ID: {course_id})")
            
            # Create a test exam for this course
            insert_exam_query = text("""
                INSERT INTO exams (course_id, grupa_name, date, time, sala_name, status)
                VALUES (:course_id, :grupa_name, :date, :time, :sala_name, :status)
                ON CONFLICT (id) DO NOTHING
                RETURNING id
            """)
            
            exam_result = connection.execute(insert_exam_query, {
                "course_id": course_id,
                "grupa_name": "CS101",
                "date": "2025-06-15",
                "time": "10:00:00",
                "sala_name": "C305",
                "status": "CONFIRMED"
            })
            
            exam = exam_result.fetchone()
            if exam:
                print(f"Created exam (ID: {exam[0]}) for course {course_name}")
            else:
                # Check if exam already exists
                check_exam_query = text("""
                    SELECT id FROM exams WHERE course_id = :course_id
                """)
                existing_exam = connection.execute(check_exam_query, {"course_id": course_id}).fetchone()
                if existing_exam:
                    print(f"Exam already exists (ID: {existing_exam[0]}) for course {course_name}")
                else:
                    print("Failed to create exam")
            
            # Commit the transaction
            trans.commit()
            print("All changes committed successfully")
            
        except Exception as e:
            # Rollback in case of error
            trans.rollback()
            print(f"Error: {e}")
            print("Transaction rolled back")

if __name__ == "__main__":
    print("Creating test course and exam for Professor John Smith...")
    create_professor_course()
    print("Done")
