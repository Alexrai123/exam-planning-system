import pandas as pd
import io
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.exam import Exam
from ..models.course import Course
from ..models.grupa import Grupa
from ..models.sala import Sala

def generate_exams_excel(exams: List[Exam], db: Session) -> bytes:
    """
    Generate an Excel file containing exam data
    
    Args:
        exams: List of Exam objects
        db: Database session
        
    Returns:
        Excel file as bytes
    """
    try:
        # Create a list to store the processed exam data
        exam_data = []
        
        for exam in exams:
            # Get related data
            course = db.query(Course).filter(Course.id == exam.course_id).first()
            
            # Format the exam data for Excel
            exam_row = {
                'ID': exam.id,
                'Date': exam.date,
                'Time': exam.time,
                'Course': course.name if course else f"Course {exam.course_id}",
                'Room': exam.sala_name,
                'Group': exam.grupa_name,
                'Status': exam.status,
                'Professor': course.profesor_name if course and hasattr(course, 'profesor_name') else 'N/A',
                'Faculty': getattr(course, 'faculty_name', 'N/A') if course else 'N/A'
            }
            
            exam_data.append(exam_row)
        
        # Create a DataFrame from the exam data
        df = pd.DataFrame(exam_data)
        
        # Create an Excel file in memory
        output = io.BytesIO()
        
        # Create a writer to save the Excel file
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Exams', index=False)
            
            # Get the worksheet and format it
            workbook = writer.book
            worksheet = writer.sheets['Exams']
            
            # Add some formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Write the column headers with the defined format
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Adjust column widths
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)
        
        # Get the Excel file as bytes
        output.seek(0)
        return output.getvalue()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Excel file: {str(e)}")
