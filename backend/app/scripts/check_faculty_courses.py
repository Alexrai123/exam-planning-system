import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create a direct database connection
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/exam_planning"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_faculty_courses():
    print("Checking courses by faculty...")
    
    # Get DB session
    db = SessionLocal()
    
    try:
        # Get all faculties
        faculties_result = db.execute(text("SELECT id, name FROM faculties")).fetchall()
        
        print(f"Found {len(faculties_result)} faculties:")
        for faculty in faculties_result:
            faculty_id, faculty_name = faculty
            print(f"Faculty: {faculty_name} (ID: {faculty_id})")
            
            # Get courses for this faculty
            courses_result = db.execute(
                text("SELECT id, name, faculty_id FROM courses WHERE faculty_id = :faculty_id"),
                {"faculty_id": faculty_id}
            ).fetchall()
            
            print(f"  Courses for {faculty_name}: {len(courses_result)}")
            for course in courses_result:
                course_id, course_name, course_faculty_id = course
                print(f"    - {course_name} (ID: {course_id})")
            
            # If no courses found for this faculty, add some sample courses
            if len(courses_result) == 0 and faculty_name == "FIESC":
                print(f"  No courses found for {faculty_name}. Adding sample courses...")
                
                # Sample courses for FIESC faculty
                sample_courses = [
                    "Introduction to Electrical Engineering",
                    "Digital Electronics",
                    "Power Systems",
                    "Control Systems",
                    "Microprocessors and Microcontrollers",
                    "Signals and Systems",
                    "Electrical Machines",
                    "Power Electronics",
                    "Communication Systems",
                    "VLSI Design"
                ]
                
                for course_name in sample_courses:
                    db.execute(
                        text("INSERT INTO courses (name, faculty_id) VALUES (:name, :faculty_id)"),
                        {"name": course_name, "faculty_id": faculty_id}
                    )
                
                db.commit()
                print(f"  Added {len(sample_courses)} sample courses to {faculty_name}")
        
        # Check for courses with no faculty
        no_faculty_courses = db.execute(
            text("SELECT id, name FROM courses WHERE faculty_id IS NULL OR faculty_id = ''")
        ).fetchall()
        
        print(f"\nCourses with no faculty assigned: {len(no_faculty_courses)}")
        for course in no_faculty_courses:
            course_id, course_name = course
            print(f"  - {course_name} (ID: {course_id})")
            
    except Exception as e:
        print(f"Error checking faculty courses: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_faculty_courses()
