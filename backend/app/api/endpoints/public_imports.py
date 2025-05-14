"""
Public API endpoints for importing data from Excel files (no authentication required)
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from typing import List, Optional
from sqlalchemy.orm import Session
import pandas as pd
import io
import datetime

from app.api import deps
from app.models.exam import Exam, ExamStatus
from app.models.course import Course
from app.models.grupa import Grupa
from app.models.sala import Sala
from app.models.faculty import Faculty
from app.models.professor import Professor
from app.db.base import get_db

router = APIRouter()

@router.post("/exams", status_code=200)
async def import_exams_from_excel(
    file: UploadFile = File(...),
    response: Response = None,
):
    # Get database session
    db = next(get_db())
    
    # Pre-load all faculties to avoid conflicts
    all_faculties = {faculty.name: faculty for faculty in db.query(Faculty).all()}
    print(f"Loaded {len(all_faculties)} existing faculties")
    """
    Import exams from Excel file (public endpoint, no authentication required)
    """
    # Add CORS headers to response
    if response:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    try:
        print(f"Processing exam import from public endpoint")
        
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
        # For date, check for either format column
        date_columns = ["Date (YYYY-MM-DD)", "Date (DD/MM/YYYY)"]
        time_columns = ["Time (HH:MM)"]
        other_required_columns = ["Room", "Group"]
        # Course and professor checks are handled below in the missing_columns section
            
        missing_columns = []  
        
        # Check for date column - need at least one of the date formats
        if not any(col in df.columns for col in date_columns):
            missing_columns.append("Date (YYYY-MM-DD) or Date (DD/MM/YYYY)")
            
        # Check for time column
        if not any(col in df.columns for col in time_columns):
            missing_columns.append("Time (HH:MM)")
            
        # Check other required columns
        for col in other_required_columns:
            if col not in df.columns:
                missing_columns.append(col)
                
        # Special handling for course and professor columns
        if "Course Name" not in df.columns and "Course" not in df.columns:
            missing_columns.append("Course Name or Course")
            
        if "Professor Name" not in df.columns and "Professor" not in df.columns:
            missing_columns.append("Professor Name or Professor")
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
                
                # Get professor information
                professor_name = None
                if "Professor Name" in row.index:
                    professor_name = row["Professor Name"]
                elif "Professor" in row.index:
                    professor_name = row["Professor"]
                
                # Get faculty information
                faculty_name = None
                if "Faculty" in row.index:
                    faculty_name = row["Faculty"]
                
                # Get specialization information
                specialization_name = None
                if "Specialization" in row.index:
                    specialization_name = row["Specialization"]
                
                # If course doesn't exist, create it with the available information
                if not course:
                    # Try to find or use faculty
                    faculty = None
                    if faculty_name:
                        # Check if we already have this faculty in our pre-loaded list
                        if faculty_name in all_faculties:
                            faculty = all_faculties[faculty_name]
                            print(f"Using existing faculty: {faculty.name} with ID {faculty.id}")
                        else:
                            # Use a default faculty if available
                            if all_faculties:
                                # Use the first available faculty
                                faculty = list(all_faculties.values())[0]
                                print(f"Using default faculty: {faculty.name} with ID {faculty.id}")
                            else:
                                # If no faculties exist, we'll proceed without a faculty
                                print("No faculties available, proceeding without faculty")
                                faculty = None
                    
                    # Create the course
                    new_course_data = {
                        "name": course_name,
                        "profesor_name": professor_name if professor_name else "N/A",  # Default professor
                    }
                    
                    # Add faculty ID if available
                    if faculty:
                        new_course_data["faculty_id"] = faculty.id
                        
                    # Create the course
                    course = Course(**new_course_data)
                    db.add(course)
                    db.flush()
                    print(f"Created new course: {course_name}")
                    
                    # Store specialization directly in the course description if available
                    if specialization_name:
                        course.description = f"Specialization: {specialization_name}"
                        db.flush()
                        print(f"Added specialization {specialization_name} to course {course_name}")
                
                # Update existing course with faculty and specialization if needed
                elif faculty_name or specialization_name:
                    # Update faculty if provided
                    if faculty_name:
                        # Check if we already have this faculty in our pre-loaded list
                        if faculty_name in all_faculties:
                            faculty = all_faculties[faculty_name]
                            print(f"Using existing faculty: {faculty.name} with ID {faculty.id}")
                            
                            # Update course with faculty ID
                            course.faculty_id = faculty.id
                            db.flush()
                            print(f"Updated course {course_name} with faculty {faculty_name}")
                        else:
                            # Use a default faculty if available
                            if all_faculties:
                                # Use the first available faculty
                                faculty = list(all_faculties.values())[0]
                                course.faculty_id = faculty.id
                                db.flush()
                                print(f"Updated course {course_name} with default faculty {faculty.name}")
                            else:
                                # If no faculties exist, we'll proceed without updating the faculty
                                print(f"No faculties available, not updating faculty for course {course_name}")
                    
                    # Update specialization if provided
                    if specialization_name:
                        course.description = f"Specialization: {specialization_name}"
                        db.flush()
                        print(f"Updated course {course_name} with specialization {specialization_name}")
                
                # If professor is specified, find or create the professor
                professor = None
                if professor_name and professor_name.lower() not in ['n/a', 'none', '']:
                    professor = db.query(Professor).filter(Professor.name == professor_name).first()
                    if not professor:
                        # Create new professor
                        professor = Professor(name=professor_name)
                        db.add(professor)
                        db.flush()
                        print(f"Created new professor: {professor_name}")
                
                # Update course with professor if needed
                if professor and course:
                    # Use professor name instead of id since name is the primary key
                    course.professor_name = professor.name
                    db.flush()
                
                # Parse date and time
                try:
                    # Check which date column exists in the dataframe
                    if "Date (YYYY-MM-DD)" in df.columns:
                        date_column = "Date (YYYY-MM-DD)"
                    elif "Date (DD/MM/YYYY)" in df.columns:
                        date_column = "Date (DD/MM/YYYY)"
                    else:
                        # Default to YYYY-MM-DD format if neither column is found
                        date_column = "Date (YYYY-MM-DD)"
                        
                    exam_date_str = str(row[date_column])
                    exam_time_str = str(row["Time (HH:MM)"])
                    
                    # Check if the date string includes a timestamp (e.g., '2025-06-15 00:00:00')
                    # First try to parse as a datetime with time component
                    exam_date = None
                    
                    # Try to extract just the date part if there's a space (indicating time component)
                    if ' ' in exam_date_str:
                        try:
                            # Try to parse as a full datetime string
                            date_part = exam_date_str.split(' ')[0]  # Get just the date part
                            exam_date_str = date_part  # Use only the date part for further processing
                        except Exception:
                            # If splitting fails, continue with original string
                            pass
                    
                    # Try multiple date formats
                    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
                    
                    # Try each format until one works
                    for date_format in date_formats:
                        try:
                            exam_date = datetime.datetime.strptime(exam_date_str, date_format).date()
                            break  # Exit the loop if successful
                        except ValueError:
                            continue
                            
                    if exam_date is None:
                        raise ValueError(f"time data '{exam_date_str}' does not match any supported format. Please use YYYY-MM-DD (e.g., 2025-06-15) or DD/MM/YYYY (e.g., 15/06/2025)")
                    
                    # Parse time - handle different time formats and potential issues
                    try:
                        # Check if time string has AM/PM indicator
                        if 'AM' in exam_time_str.upper() or 'PM' in exam_time_str.upper():
                            # Try to parse 12-hour format
                            try:
                                time_obj = datetime.datetime.strptime(exam_time_str, '%I:%M %p').time()
                            except ValueError:
                                time_obj = datetime.datetime.strptime(exam_time_str, '%I:%M%p').time()
                        else:
                            # Handle potential issues with time format
                            if ':' in exam_time_str:
                                parts = exam_time_str.split(':')
                                if len(parts) >= 2:
                                    hour_str, minute_str = parts[0], parts[1]
                                    # Remove any non-numeric characters
                                    hour_str = ''.join(c for c in hour_str if c.isdigit())
                                    minute_str = ''.join(c for c in minute_str if c.isdigit())
                                    
                                    # Convert to integers with default values if conversion fails
                                    try:
                                        hour = int(hour_str) if hour_str else 0
                                        minute = int(minute_str) if minute_str else 0
                                    except ValueError:
                                        hour, minute = 0, 0
                                else:
                                    hour, minute = 0, 0
                            else:
                                # If no colon, try to interpret as a whole number of hours
                                try:
                                    hour = int(exam_time_str)
                                    minute = 0
                                except ValueError:
                                    hour, minute = 0, 0
                            
                            # Ensure hour and minute are within valid ranges
                            hour = min(max(hour, 0), 23)  # Between 0 and 23
                            minute = min(max(minute, 0), 59)  # Between 0 and 59
                            
                            time_obj = datetime.time(hour=hour, minute=minute)
                        
                        # Combine date and time
                        exam_datetime = datetime.datetime.combine(exam_date, time_obj)
                    except Exception as e:
                        raise ValueError(f"Invalid time format: '{exam_time_str}'. Please use HH:MM format (e.g., 14:30). Error: {str(e)}")
                        
                except Exception as e:
                    errors.append(f"Row {index+2}: Invalid date/time format: {str(e)}")
                    continue
                
                # Get room and group
                room_name = str(row["Room"])
                group_name = str(row["Group"])
                
                # Check if the room exists, create it if it doesn't
                room = db.query(Sala).filter(Sala.name == room_name).first()
                if not room:
                    # Create a new room
                    new_room = Sala(name=room_name, capacity=30)  # Default capacity
                    db.add(new_room)
                    db.flush()  # Flush to get the ID without committing
                    room_name = new_room.name
                else:
                    room_name = room.name
                
                # Check if the group exists, create it if it doesn't
                group = db.query(Grupa).filter(Grupa.name == group_name).first()
                if not group:
                    # Create a new group
                    new_group = Grupa(name=group_name, year=1)  # Default year
                    db.add(new_group)
                    db.flush()  # Flush to get the ID without committing
                    group_name = new_group.name
                else:
                    group_name = group.name
                
                existing_exam = db.query(Exam).filter(
                    Exam.course_id == course.id,
                    Exam.date == exam_datetime.date(),
                    Exam.time == exam_datetime.time()
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
                status = ExamStatus.PROPOSED
                if "Status" in df.columns and row["Status"]:
                    # Convert string status to enum value
                    status_str = str(row["Status"]).strip().upper()
                    if status_str in ["CONFIRMED", "CONFIRM"]:
                        status = ExamStatus.CONFIRMED
                    elif status_str in ["CANCELLED", "CANCEL"]:
                        status = ExamStatus.CANCELLED
                    elif status_str in ["COMPLETED", "COMPLETE"]:
                        status = ExamStatus.COMPLETED
                    else:
                        status = ExamStatus.PROPOSED
                
                if existing_exam:
                    # Update existing exam
                    existing_exam.sala_name = room_name
                    existing_exam.grupa_name = group_name
                    existing_exam.date = exam_datetime.date()  # Extract just the date part
                    existing_exam.time = exam_datetime.time()  # Extract just the time part
                    existing_exam.status = status
                    existing_exam.professor_agreement = professor_agreement
                    exams_updated += 1
                else:
                    # Create new exam
                    new_exam = Exam(
                        course_id=course.id,
                        date=exam_datetime.date(),  # Extract just the date part
                        time=exam_datetime.time(),   # Extract just the time part
                        sala_name=room_name,
                        grupa_name=group_name,
                        status=status,
                        professor_agreement=professor_agreement
                    )
                    db.add(new_exam)
                    exams_created += 1
            
            except Exception as e:
                errors.append(f"Row {index+2}: {str(e)}")
        
        # Commit changes
        db.commit()
        
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
