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

def add_fiesc_courses():
    print("Adding courses for FIESC faculty...")
    
    # Get DB session
    db = SessionLocal()
    
    try:
        # First, check if FIESC faculty exists
        fiesc_faculty = db.execute(
            text("SELECT id, name FROM faculties WHERE name LIKE '%FIESC%'")
        ).fetchone()
        
        faculty_id = None
        
        if fiesc_faculty:
            faculty_id = fiesc_faculty[0]
            print(f"Found existing faculty: {fiesc_faculty[1]} (ID: {faculty_id})")
        else:
            # Get the next ID from the sequence
            print("FIESC faculty not found. Let's create a new one.")
            # First, get all faculties to find the highest ID
            all_faculties = db.execute(text("SELECT id, name FROM faculties ORDER BY id")).fetchall()
            
            if all_faculties:
                # Find the highest ID
                highest_id = max(faculty[0] for faculty in all_faculties)
                new_id = highest_id + 1
                print(f"Highest faculty ID: {highest_id}, will use {new_id} for FIESC")
                
                # Create FIESC faculty with explicit ID
                db.execute(
                    text("INSERT INTO faculties (id, name) VALUES (:id, :name)"),
                    {"id": new_id, "name": "FIESC"}
                )
                faculty_id = new_id
                db.commit()
                print(f"Created new faculty: FIESC (ID: {faculty_id})")
            else:
                print("No faculties found in the database.")
                return
        
        if not faculty_id:
            print("Could not determine faculty ID. Aborting.")
            return
            
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
            "VLSI Design",
            "Computer Networks",
            "Embedded Systems",
            "Robotics",
            "Automation Systems",
            "Internet of Things"
        ]
        
        # Add courses for FIESC faculty
        added_courses = 0
        for course_name in sample_courses:
            # Check if course already exists
            existing_course = db.execute(
                text("SELECT id FROM courses WHERE name = :name"),
                {"name": course_name}
            ).fetchone()
            
            if not existing_course:
                # Get the next ID for courses
                all_courses = db.execute(text("SELECT id FROM courses ORDER BY id DESC LIMIT 1")).fetchone()
                next_id = 1
                if all_courses:
                    next_id = all_courses[0] + 1
                
                # Add new course with explicit ID
                db.execute(
                    text("INSERT INTO courses (id, name, faculty_id) VALUES (:id, :name, :faculty_id)"),
                    {"id": next_id, "name": course_name, "faculty_id": faculty_id}
                )
                added_courses += 1
                print(f"Added course: {course_name} (ID: {next_id})")
        
        db.commit()
        print(f"Added {added_courses} new courses to FIESC faculty")
        
        # Verify courses were added
        fiesc_courses = db.execute(
            text("SELECT id, name FROM courses WHERE faculty_id = :faculty_id"),
            {"faculty_id": faculty_id}
        ).fetchall()
        
        print(f"\nCourses for FIESC faculty (ID: {faculty_id}):")
        for course in fiesc_courses:
            course_id, course_name = course
            print(f"  - {course_name} (ID: {course_id})")
            
    except Exception as e:
        db.rollback()
        print(f"Error adding FIESC courses: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    add_fiesc_courses()
