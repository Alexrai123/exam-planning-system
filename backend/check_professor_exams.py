import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters for Docker environment
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "exam_planning_db"  # Use the Docker container name as the host
DB_PORT = "5432"
DB_NAME = "exam_planning"

# Create database connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def check_professor_exams(professor_name):
    """Check exams associated with a specific professor."""
    with engine.connect() as connection:
        # First, get the courses taught by this professor
        courses_query = text("""
            SELECT id, name, profesor_name 
            FROM courses 
            WHERE profesor_name = :professor_name
        """)
        
        courses_result = connection.execute(courses_query, {"professor_name": professor_name})
        courses = []
        for row in courses_result:
            courses.append({"id": row[0], "name": row[1], "profesor_name": row[2]})
        
        print(f"\nCourses taught by {professor_name}:")
        if not courses:
            print("No courses found for this professor.")
            return
            
        for course in courses:
            print(f"- Course ID: {course['id']}, Name: {course['name']}")
        
        # Get course IDs
        course_ids = [course['id'] for course in courses]
        
        if not course_ids:
            print("No course IDs found to query exams.")
            return
            
        # Now get exams for these courses
        placeholders = ', '.join([f':id{i}' for i in range(len(course_ids))])
        params = {f'id{i}': id for i, id in enumerate(course_ids)}
        
        exams_query = text(f"""
            SELECT e.id, e.course_id, e.date, e.time, e.sala_name, e.grupa_name, e.status,
                   c.name as course_name
            FROM exams e
            JOIN courses c ON e.course_id = c.id
            WHERE e.course_id IN ({placeholders})
        """)
        
        exams_result = connection.execute(exams_query, params)
        exams = []
        for row in exams_result:
            exams.append({
                "id": row[0],
                "course_id": row[1],
                "date": row[2],
                "time": row[3],
                "sala_name": row[4],
                "grupa_name": row[5],
                "status": row[6],
                "course_name": row[7]
            })
        
        print(f"\nExams for {professor_name}:")
        if not exams:
            print("No exams found for this professor's courses.")
            return
            
        for exam in exams:
            print(f"- Exam ID: {exam['id']}")
            print(f"  Course: {exam['course_name']} (ID: {exam['course_id']})")
            print(f"  Date/Time: {exam['date']} at {exam['time']}")
            print(f"  Room: {exam['sala_name']}")
            print(f"  Group: {exam['grupa_name']}")
            print(f"  Status: {exam['status']}")
            print()

if __name__ == "__main__":
    professor_name = "John Smith"
    print(f"Checking exams for professor: {professor_name}")
    check_professor_exams(professor_name)
