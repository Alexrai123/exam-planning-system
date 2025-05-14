import psycopg2

# Database connection parameters
DB_PARAMS = {
    'dbname': 'exam_planning',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'postgres',
    'port': '5432'
}

# Sample courses for FIESC faculty
FIESC_COURSES = [
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

def main():
    print("Adding courses for FIESC faculty...")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Check if FIESC faculty exists
        cursor.execute("SELECT id, name FROM faculties WHERE name LIKE '%FIESC%'")
        fiesc_faculty = cursor.fetchone()
        
        faculty_id = None
        
        if fiesc_faculty:
            faculty_id = fiesc_faculty[0]
            print(f"Found existing faculty: {fiesc_faculty[1]} (ID: {faculty_id})")
        else:
            print("FIESC faculty not found. Creating new faculty...")
            # Get the next ID from the sequence
            cursor.execute("SELECT MAX(id) FROM faculties")
            max_id = cursor.fetchone()[0]
            new_id = 1 if max_id is None else max_id + 1
            
            # Insert new faculty
            cursor.execute(
                "INSERT INTO faculties (id, name) VALUES (%s, %s) RETURNING id",
                (new_id, "FIESC")
            )
            faculty_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Created new faculty: FIESC (ID: {faculty_id})")
        
        # Add courses for FIESC faculty
        added_courses = 0
        for course_name in FIESC_COURSES:
            # Check if course already exists
            cursor.execute(
                "SELECT id FROM courses WHERE name = %s",
                (course_name,)
            )
            existing_course = cursor.fetchone()
            
            if not existing_course:
                # Get the next ID for courses
                cursor.execute("SELECT MAX(id) FROM courses")
                max_id = cursor.fetchone()[0]
                new_id = 1 if max_id is None else max_id + 1
                
                # Insert new course
                cursor.execute(
                    "INSERT INTO courses (id, name, faculty_id) VALUES (%s, %s, %s) RETURNING id",
                    (new_id, course_name, faculty_id)
                )
                course_id = cursor.fetchone()[0]
                conn.commit()
                added_courses += 1
                print(f"Added course: {course_name} (ID: {course_id})")
        
        print(f"Added {added_courses} new courses to FIESC faculty")
        
        # Verify courses were added
        cursor.execute(
            "SELECT id, name FROM courses WHERE faculty_id = %s",
            (faculty_id,)
        )
        fiesc_courses = cursor.fetchall()
        
        print(f"\nCourses for FIESC faculty (ID: {faculty_id}):")
        for course in fiesc_courses:
            course_id, course_name = course
            print(f"  - {course_name} (ID: {course_id})")
            
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error adding FIESC courses: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
