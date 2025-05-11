import io
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

from ..models.exam import Exam
from ..models.course import Course

def generate_exams_pdf(exams: List[Exam], db: Session) -> bytes:
    """
    Generate a PDF file containing confirmed exam data
    
    Args:
        exams: List of Exam objects
        db: Database session
        
    Returns:
        PDF file as bytes
    """
    try:
        # Filter to only include confirmed exams
        # The status can be either a string 'ExamStatus.CONFIRMED' or an enum value ExamStatus.CONFIRMED
        confirmed_exams = []
        for exam in exams:
            # Check different possible formats of confirmed status
            if str(exam.status) == "ExamStatus.CONFIRMED" or \
               str(exam.status) == "confirmed" or \
               (hasattr(exam.status, "value") and exam.status.value == "confirmed"):
                confirmed_exams.append(exam)
        
        # Ensure all confirmed exams have professor_agreement set to True
        for exam in confirmed_exams:
            if not exam.professor_agreement:
                exam.professor_agreement = True
                db.add(exam)
        
        # Commit changes if any were made
        db.commit()
        
        # If no confirmed exams, return empty PDF with message
        if not confirmed_exams:
            # Create a buffer to store the PDF
            buffer = io.BytesIO()
            
            # Create the PDF document with landscape orientation
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
            
            # Get the default styles
            styles = getSampleStyleSheet()
            
            # Create the document elements
            elements = []
            elements.append(Paragraph("No confirmed exams found", styles['Heading1']))
            
            # Build the PDF
            doc.build(elements)
            
            # Get the PDF content
            pdf_content = buffer.getvalue()
            buffer.close()
            
            return pdf_content
        
        # Use confirmed exams for the rest of the function
        exams = confirmed_exams
        
        # Create a buffer to store the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document with landscape orientation
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        
        # Get the default styles and create custom styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.darkblue
        )
        normal_style = styles['Normal']
        
        # Create the document elements
        elements = []
        
        # Add university header
        elements.append(Paragraph("University Exam Planning System", title_style))
        elements.append(Paragraph("Official Confirmed Exam Schedule", subtitle_style))
        elements.append(Spacer(1, 12))
        
        # Add semester and academic year info
        current_year = datetime.now().year
        academic_year = f"{current_year-1}-{current_year}" if datetime.now().month < 9 else f"{current_year}-{current_year+1}"
        semester = "Second Semester" if datetime.now().month > 1 and datetime.now().month < 9 else "First Semester"
        
        elements.append(Paragraph(f"Academic Year: {academic_year} - {semester}", normal_style))
        elements.append(Spacer(1, 6))
        
        # Add generation date and time
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"Generated on: {current_date}", normal_style))
        elements.append(Spacer(1, 12))
        
        # Prepare data for the table
        data = [['Date', 'Time', 'Course', 'Professor', 'Room', 'Group']]
        
        for exam in exams:
            # Get related data
            course = db.query(Course).filter(Course.id == exam.course_id).first()
            
            # Format the date
            formatted_date = exam.date.strftime('%Y-%m-%d') if exam.date else 'N/A'
            
            # Format the status (remove the enum prefix if present)
            status_value = exam.status
            if status_value and '.' in status_value:
                status_value = status_value.split('.')[-1]  # Get the part after the last dot
            
            # Capitalize the status for better presentation
            if status_value:
                status_value = status_value.capitalize()
            
            # Get course name without professor name
            course_name = "N/A"
            if course and hasattr(course, 'name'):
                # If course name contains professor name (with a dash), remove it
                if ' - ' in course.name:
                    course_name = course.name.split(' - ')[0].strip()
                else:
                    course_name = course.name
            else:
                course_name = f"Course {exam.course_id}"
            
            # Get professor name
            professor_name = course.profesor_name if course and hasattr(course, 'profesor_name') else 'N/A'
            
            # Add the exam data to the table
            data.append([
                formatted_date,
                exam.time or 'N/A',
                course_name,
                professor_name,
                exam.sala_name or 'N/A',
                exam.grupa_name or 'N/A'
            ])
        
        # Calculate column widths based on content and available space
        # Landscape letter size is 11x8.5 inches, with margins we have about 10x7.5 inches
        available_width = 10 * 72  # 10 inches in points
        col_widths = [80, 70, 200, 160, 70, 70]  # Adjusted column widths for 6 columns
        
        # Create the table with specified column widths
        table = Table(data, colWidths=col_widths, repeatRows=1)  # Repeat header row on all pages
        
        # Add style to the table
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWHEIGHT', (0, 0), (-1, 0), 30),
            ('ROWHEIGHT', (0, 1), (-1, -1), 30),  # Increased row height for better readability
            # Add word wrapping for course names (column 3)
            ('WORDWRAP', (3, 0), (3, -1), True)
        ])
        
        # Apply alternating row colors
        for i in range(1, len(data)):
            if i % 2 == 0:
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
        
        table.setStyle(table_style)
        
        # Add the table to the elements
        elements.append(table)
        
        # Build the PDF
        doc.build(elements)
        
        # Get the PDF as bytes
        buffer.seek(0)
        return buffer.getvalue()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF file: {str(e)}")
