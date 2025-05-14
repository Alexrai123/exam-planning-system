"""
Script to add sample exams to the database
"""
from app.db.base import get_db
from sqlalchemy import text
import datetime

def main():
    # Get database connection
    db = next(get_db())
    
    # Sample exams data
    sample_exams = [
        {
            "course_id": 154,  # Semiologia aparatului cardio-vascular: valvulopatii, HTA
            "date": "2025-06-15",
            "time": "10:00",
            "sala_name": "C101",
            "grupa_name": "3111",
            "status": "PROPOSED",
            "professor_agreement": False,
            "publication_date": None
        },
        {
            "course_id": 112,  # Anatomie
            "date": "2025-06-18",
            "time": "14:00",
            "sala_name": "C102",
            "grupa_name": "3112",
            "status": "CONFIRMED",
            "professor_agreement": True,
            "publication_date": datetime.datetime.now().strftime("%Y-%m-%d")
        },
        {
            "course_id": 114,  # Biochimie
            "date": "2025-06-20",
            "time": "09:00",
            "sala_name": "C103",
            "grupa_name": "3113",
            "status": "PROPOSED",
            "professor_agreement": False,
            "publication_date": None
        }
    ]
    
    # Insert exams into the database
    for exam in sample_exams:
        # Check if the course exists
        course_query = text("SELECT id, name FROM courses WHERE id = :course_id")
        course = db.execute(course_query, {"course_id": exam["course_id"]}).fetchone()
        
        if not course:
            print(f"Course with ID {exam['course_id']} not found, skipping exam")
            continue
        
        # Check if the room exists
        room_query = text("SELECT name FROM sala WHERE name = :sala_name")
        room = db.execute(room_query, {"sala_name": exam["sala_name"]}).fetchone()
        
        if not room:
            print(f"Room {exam['sala_name']} not found, skipping exam")
            continue
        
        # Check if the group exists
        group_query = text("SELECT name FROM grupa WHERE name = :grupa_name")
        group = db.execute(group_query, {"grupa_name": exam["grupa_name"]}).fetchone()
        
        if not group:
            print(f"Group {exam['grupa_name']} not found, skipping exam")
            continue
        
        # Combine date and time
        date_time = f"{exam['date']} {exam['time']}"
        
        # Check if an exam already exists for this course and date
        existing_query = text("""
            SELECT id FROM exams 
            WHERE course_id = :course_id 
            AND CAST(date AS DATE) = CAST(:date AS DATE)
        """)
        existing = db.execute(existing_query, {
            "course_id": exam["course_id"],
            "date": exam["date"]
        }).fetchone()
        
        if existing:
            print(f"Exam for course {course[1]} on {exam['date']} already exists, skipping")
            continue
        
        # Insert the exam
        insert_query = text("""
            INSERT INTO exams (
                course_id, date, time, sala_name, grupa_name, 
                status, professor_agreement, publication_date
            ) VALUES (
                :course_id, :date, :time, :sala_name, :grupa_name,
                :status, :professor_agreement, :publication_date
            )
        """)
        
        try:
            db.execute(insert_query, {
                "course_id": exam["course_id"],
                "date": exam["date"],
                "time": exam["time"],
                "sala_name": exam["sala_name"],
                "grupa_name": exam["grupa_name"],
                "status": exam["status"],
                "professor_agreement": exam["professor_agreement"],
                "publication_date": exam["publication_date"]
            })
            db.commit()
            print(f"Added exam for course {course[1]} on {exam['date']} at {exam['time']}")
        except Exception as e:
            db.rollback()
            print(f"Error adding exam for course {course[1]}: {str(e)}")
    
    # Verify the exams were added
    print("\nExams in the database:")
    exams_query = text("""
        SELECT e.id, c.name, e.date, e.time, e.sala_name, e.grupa_name, e.status, e.professor_agreement
        FROM exams e
        JOIN courses c ON e.course_id = c.id
        ORDER BY e.date
    """)
    exams = db.execute(exams_query).fetchall()
    for exam in exams:
        print(f"ID: {exam[0]}, Course: {exam[1]}, Date: {exam[2]}, Time: {exam[3]}, Room: {exam[4]}, Group: {exam[5]}, Status: {exam[6]}, Professor Agreement: {exam[7]}")

if __name__ == "__main__":
    main()
