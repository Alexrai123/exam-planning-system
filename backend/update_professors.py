"""
Script to update courses with professor names and update exams
"""
from app.db.base import get_db
from sqlalchemy import text

def main():
    # Get database connection
    db = next(get_db())
    
    # Get some professor names from the database
    print("Getting professors from database...")
    professors_query = text("SELECT name FROM professors LIMIT 5")
    professors = db.execute(professors_query).fetchall()
    professor_names = [prof[0] for prof in professors]
    
    if not professor_names:
        print("No professors found in the database!")
        return
    
    # Update courses with professor names
    print("\nUpdating courses with professor names...")
    courses_to_update = [
        {"id": 154, "professor": professor_names[0]},  # Semiologia aparatului cardio-vascular: valvulopatii, HTA
        {"id": 112, "professor": professor_names[1]},  # Anatomie
        {"id": 114, "professor": professor_names[2]}   # Biochimie
    ]
    
    for course in courses_to_update:
        update_query = text("""
            UPDATE courses
            SET profesor_name = :professor_name
            WHERE id = :course_id
        """)
        
        try:
            db.execute(update_query, {
                "professor_name": course["professor"],
                "course_id": course["id"]
            })
            db.commit()
            print(f"Updated course ID {course['id']} with professor {course['professor']}")
        except Exception as e:
            db.rollback()
            print(f"Error updating course ID {course['id']}: {str(e)}")
    
    # Verify the courses were updated
    print("\nVerifying updated courses:")
    courses_query = text("""
        SELECT id, name, profesor_name 
        FROM courses 
        WHERE id IN (154, 112, 114)
    """)
    courses = db.execute(courses_query).fetchall()
    for course in courses:
        print(f"ID: {course[0]}, Course: {course[1]}, Professor: {course[2]}")
    
    # Verify the exams reflect the updated professor information
    print("\nVerifying exams with updated professor information:")
    exams_query = text("""
        SELECT e.id, c.name, c.profesor_name, e.date, e.time, e.sala_name, e.grupa_name, e.status, e.professor_agreement
        FROM exams e
        JOIN courses c ON e.course_id = c.id
        WHERE e.course_id IN (154, 112, 114)
        ORDER BY e.date
    """)
    exams = db.execute(exams_query).fetchall()
    for exam in exams:
        print(f"ID: {exam[0]}, Course: {exam[1]}, Professor: {exam[2]}, Date: {exam[3]}, Time: {exam[4]}, Room: {exam[5]}, Group: {exam[6]}, Status: {exam[7]}, Professor Agreement: {exam[8]}")

if __name__ == "__main__":
    main()
