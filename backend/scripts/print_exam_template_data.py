"""
Script to print sample exam data for Calculatoare, ESM, and ESCCA specializations
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def print_exam_template_data():
    """
    Print sample exam data for Calculatoare, ESM, and ESCCA specializations
    """
    try:
        # Print the header row for the CSV
        header = "faculty_name,faculty_short_name,specialization_name,specialization_short_name,course_id,course_name,year,semester,grupa_name,date,time,sala_name,status"
        print(header)
        
        with engine.connect() as conn:
            # Get faculty information - using ASCII names to avoid encoding issues
            faculty_name = "Facultatea de Inginerie Electrica si Stiinta Calculatoarelor"
            faculty_short_name = "FIESC"
            
            # Get courses from Calculatoare, ESM, and ESCCA specializations
            specializations_data = [
                {"name": "Calculatoare", "short_name": "CALC"},
                {"name": "Echipamente si sisteme medicale", "short_name": "ESM"},
                {"name": "Echipamente si sisteme de comanda pentru autovehicule", "short_name": "ESCA"}
            ]
            
            for spec_data in specializations_data:
                specialization_name = spec_data["name"]
                specialization_short_name = spec_data["short_name"]
                
                # Get courses for this specialization
                result = conn.execute(text("""
                    SELECT c.id, c.name, c.year, c.semester
                    FROM courses c
                    JOIN specializations s ON c.faculty_id = s.faculty_id
                    WHERE s.name = :specialization OR s.short_name = :short_name
                    ORDER BY c.year, c.semester, c.name
                """), {"specialization": specialization_name, "short_name": specialization_short_name})
                
                courses = result.fetchall()
                
                # Generate sample rows for each specialization (5 courses per year)
                for year in range(1, 5):
                    year_courses = [c for c in courses if c[2] == year]
                    sample_courses = year_courses[:5]  # Take up to 5 courses per year
                    
                    for i, course in enumerate(sample_courses):
                        if i >= 3:  # Limit to 3 courses per year to avoid too much data
                            continue
                            
                        course_id = course[0]
                        course_name = course[1].replace(",", " ")  # Remove commas for CSV compatibility
                        course_year = course[2]
                        semester = course[3]
                        
                        # Generate sample data
                        group_name = f"{specialization_short_name}{course_year}{chr(65+i)}"
                        exam_date = datetime(2025, 6, 10) + timedelta(days=i)
                        exam_time = f"{9+i}:00"
                        room = f"C{course_year}{i+1}"
                        status = "proposed"
                        
                        # Print row for CSV
                        row = f"{faculty_name},{faculty_short_name},{specialization_name},{specialization_short_name},{course_id},{course_name},{course_year},{semester},{group_name},{exam_date.strftime('%Y-%m-%d')},{exam_time},{room},{status}"
                        print(row)
    
    except Exception as e:
        print(f"Error printing exam template data: {e}")

if __name__ == "__main__":
    print_exam_template_data()
