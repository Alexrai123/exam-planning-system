"""
API endpoints for importing data from Excel files
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from typing import List, Optional
from sqlalchemy.orm import Session
import pandas as pd
import io
import datetime

from app.api import deps
from app.models.user import User, UserRole
from app.models.exam import Exam
from app.models.course import Course
from app.db.base import get_db

router = APIRouter()

@router.post("/exams", status_code=200)
async def import_exams_from_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user_with_roles([UserRole.SECRETARIAT, UserRole.ADMIN])),
    db: Session = Depends(deps.get_db_dependency),
    response: Response = None,
):
    """
    Import exams from Excel file
    """
    try:
        print(f"Processing exam import for user: {current_user.email}")
        
        # Check file extension
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are allowed")
        
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Print column headers for debugging
        print(f"Excel file columns: {list(df.columns)}")
        
        # Check if this is the reordered template or the original template
        if "Course" in df.columns and "Professor" in df.columns:
            print("Detected reordered template format")
            # Map reordered template columns to expected columns
            if "Course Name" not in df.columns:
                df["Course Name"] = df["Course"]
            if "Professor Name" not in df.columns:
                df["Professor Name"] = df["Professor"]
        
        # Validate required columns - support both original and reordered formats
        required_columns = ["Date (YYYY-MM-DD)", "Time (HH:MM)", "Room", "Group"]
        # For course and professor, check both possible column names
        if "Course Name" not in df.columns and "Course" not in df.columns:
            required_columns.append("Course Name")
        if "Professor Name" not in df.columns and "Professor" not in df.columns:
            required_columns.append("Professor Name")
            
        missing_columns = []  
        for col in required_columns:
            # Special handling for course and professor columns
            if col == "Course Name" and ("Course Name" not in df.columns and "Course" not in df.columns):
                missing_columns.append("Course Name or Course")
            elif col == "Professor Name" and ("Professor Name" not in df.columns and "Professor" not in df.columns):
                missing_columns.append("Professor Name or Professor")
            # Standard check for other columns
            elif col not in df.columns:
                missing_columns.append(col)
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process data
        exams_created = 0
        exams_updated = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Find the course - support both column naming conventions
                course_name = row["Course Name"] if "Course Name" in row.index else row["Course"]
                course = db.query(Course).filter(Course.name == course_name).first()
                
                if not course:
                    errors.append(f"Row {index+2}: Course '{course_name}' not found")
                    continue
                
                # Parse date and time
                try:
                    exam_date_str = str(row["Date (YYYY-MM-DD)"])
                    exam_time_str = str(row["Time (HH:MM)"])
                    
                    # Handle different date formats
                    try:
                        exam_date = datetime.datetime.strptime(exam_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        exam_date = datetime.datetime.strptime(exam_date_str, "%d/%m/%Y").date()
                    
                    # Parse time
                    hour, minute = map(int, exam_time_str.split(':'))
                    exam_datetime = datetime.datetime.combine(
                        exam_date, 
                        datetime.time(hour=hour, minute=minute)
                    )
                except Exception as e:
                    errors.append(f"Row {index+2}: Invalid date/time format: {str(e)}")
                    continue
                
                # Get room and group
                room = row["Room"]
                group = row["Group"]
                
                # Check if exam already exists
                existing_exam = db.query(Exam).filter(
                    Exam.course_id == course.id,
                    Exam.date == exam_datetime
                ).first()
                
                # Get professor agreement status if available
                professor_agreement = False
                if "Professor Agreement" in df.columns:
                    agreement_value = row["Professor Agreement"]
                    if isinstance(agreement_value, str):
                        professor_agreement = agreement_value.upper() in ["TRUE", "YES", "Y", "1"]
                    else:
                        professor_agreement = bool(agreement_value)
                
                # Get status if available
                status = "PROPOSED"
                if "Status" in df.columns and row["Status"]:
                    status = row["Status"]
                
                if existing_exam:
                    # Update existing exam
                    existing_exam.room = room
                    existing_exam.group = group
                    existing_exam.status = status
                    existing_exam.professor_agreement = professor_agreement
                    exams_updated += 1
                else:
                    # Create new exam
                    new_exam = Exam(
                        course_id=course.id,
                        date=exam_datetime,
                        room=room,
                        group=group,
                        status=status,
                        professor_agreement=professor_agreement
                    )
                    db.add(new_exam)
                    exams_created += 1
            
            except Exception as e:
                errors.append(f"Row {index+2}: {str(e)}")
        
        # Commit changes
        db.commit()
        
        # Add CORS headers to response
        if response:
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return {
            "message": "Import completed",
            "exams_created": exams_created,
            "exams_updated": exams_updated,
            "errors": errors
        }
    
    except Exception as e:
        print(f"Error importing exams: {e}")
        # Add CORS headers even in error responses
        if response:
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        # Return a more detailed error message
        error_detail = str(e)
        if "pandas" in error_detail.lower() or "excel" in error_detail.lower():
            error_detail = "Error processing Excel file. Please ensure it follows the required format."
        elif "column" in error_detail.lower():
            error_detail = "Missing or invalid columns in Excel file. Please use the template provided."
        
        raise HTTPException(status_code=500, detail=error_detail)
