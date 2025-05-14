"""
Script to generate a CSV template for exams with faculty and specialization information
"""
import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import unicodedata

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def generate_exam_csv_template():
    """
    Generate a CSV template for exams with sample data from Calculatoare, ESM, and ESCCA specializations
    """
    try:
        # Create a dataframe to store the template data
        columns = [
            "faculty_name", "faculty_short_name", 
            "specialization_name", "specialization_short_name",
            "course_id", "course_name", "year", "semester",
            "grupa_name", "date", "time", "sala_name", "status"
        ]
        
        template_data = []
        
        with engine.connect() as conn:
            # Get faculty information
            faculty_result = conn.execute(text("SELECT id, name, short_name FROM faculties WHERE short_name = 'FIESC'"))
            faculty = faculty_result.fetchone()
            
            if not faculty:
                print("FIESC faculty not found")
                return
                
            faculty_id = faculty[0]
            faculty_name = faculty[1]
            faculty_short_name = faculty[2]
            
            print(f"Faculty: {faculty_name} ({faculty_short_name})")
            
            # Get courses from Calculatoare, ESM, and ESCCA specializations
            specializations_data = [
                {"name": "Calculatoare", "short_name": "CALC"},
                {"name": "Echipamente si sisteme medicale", "short_name": "ESM"},
                {"name": "Echipamente si sisteme de comanda pentru autovehicule", "short_name": "ESCA"}
            ]
            
            for spec_data in specializations_data:
                specialization_name = spec_data["name"]
                specialization_short_name = spec_data["short_name"]
                
                # Get specialization ID
                spec_result = conn.execute(text(
                    "SELECT id FROM specializations WHERE name = :name AND faculty_id = :faculty_id"
                ), {"name": specialization_name, "faculty_id": faculty_id})
                spec_row = spec_result.fetchone()
                
                if not spec_row:
                    print(f"Specialization {specialization_name} not found")
                    continue
                
                specialization_id = spec_row[0]
                
                # Get courses for this specialization
                result = conn.execute(text("""
                    SELECT c.id, c.name, c.year, c.semester, c.profesor_name 
                    FROM courses c
                    JOIN specializations s ON c.faculty_id = s.faculty_id
                    WHERE s.name = :specialization
                    ORDER BY c.year, c.semester, c.name
                """), {"specialization": specialization_name})
                
                courses = result.fetchall()
                
                print(f"\n{specialization_name} ({specialization_short_name}) Courses: {len(courses)}")
                
                # Generate sample rows for each specialization (5 courses per year)
                for year in range(1, 5):
                    year_courses = [c for c in courses if c[2] == year]
                    sample_courses = year_courses[:5]  # Take up to 5 courses per year
                    
                    for i, course in enumerate(sample_courses):
                        course_id = course[0]
                        course_name = course[1]
                        course_year = course[2]
                        semester = course[3]
                        
                        # Generate sample data
                        group_name = f"{specialization_short_name}{course_year}{chr(65+i)}"
                        exam_date = datetime(2025, 6, 10) + timedelta(days=i)
                        exam_time = f"{9+i:02d}:00:00"
                        room = f"C{course_year}{i+1}"
                        status = "proposed"
                        
                        # Add row to template data
                        template_data.append([
                            faculty_name, faculty_short_name,
                            specialization_name, specialization_short_name,
                            course_id, course_name, course_year, semester,
                            group_name, exam_date.strftime("%Y-%m-%d"), exam_time, room, status
                        ])
            
            # Create DataFrame and save to Excel
            df = pd.DataFrame(template_data, columns=columns)
            
            # Create output directory if it doesn't exist
            output_dir = Path(__file__).parent.parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            # Convert Romanian characters to ASCII for compatibility
            def remove_accents(input_str):
                if isinstance(input_str, str):
                    nfkd_form = unicodedata.normalize('NFKD', input_str)
                    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
                return input_str
                
            # Apply the function to all string columns
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].apply(remove_accents)
                
            # Save to CSV
            csv_path = output_dir / "exam_template.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            print(f"\nCSV template generated: {csv_path}")
            print(f"Template contains {len(template_data)} sample exam entries")
            
            # Display sample of the data
            print("\nSample rows from the template:")
            print("-" * 100)
            for i, row in enumerate(template_data[:5]):
                print(f"Row {i+1}: {row}")
            
    except Exception as e:
        print(f"Error generating Excel template: {e}")

if __name__ == "__main__":
    generate_exam_csv_template()
