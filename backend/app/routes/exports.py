from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from datetime import date
import pandas as pd
import io

from ..db.base import get_db
from ..models.exam import Exam
from ..models.course import Course
from ..models.sala import Sala
from ..models.grupa import Grupa
from ..models.user import User
from ..routes.auth import get_current_user

router = APIRouter(prefix="/exports", tags=["Exports"])

@router.get("/schedule")
def export_exam_schedule(
    response: Response,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    course_id: Optional[int] = None,
    grupa_id: Optional[int] = None,
    format: str = "excel"
) -> Any:
    """
    Export exam schedule as Excel file.
    All authenticated users can access this endpoint.
    """
    try:
        # Build query
        query = db.query(
            Exam.id,
            Exam.date,
            Exam.time,
            Exam.status,
            Course.name.label("course_name"),
            User.name.label("professor_name"),
            Grupa.name.label("group_name"),
            Sala.name.label("room_name")
        ).join(
            Course, Exam.course_id == Course.id
        ).join(
            User, Course.profesor_id == User.id
        ).join(
            Grupa, Exam.grupa_id == Grupa.id
        ).join(
            Sala, Exam.sala_id == Sala.id
        )
        
        # Apply filters
        if start_date:
            query = query.filter(Exam.date >= start_date)
        if end_date:
            query = query.filter(Exam.date <= end_date)
        if course_id:
            query = query.filter(Exam.course_id == course_id)
        if grupa_id:
            query = query.filter(Exam.grupa_id == grupa_id)
        
        # Order by date and time
        query = query.order_by(Exam.date, Exam.time)
        
        # Execute query
        results = query.all()
        
        if not results:
            # Create an empty DataFrame with the correct columns
            df = pd.DataFrame(columns=[
                'ID', 'Date', 'Time', 'Status', 'Course', 'Professor', 'Group', 'Room'
            ])
        else:
            # Convert to DataFrame
            df = pd.DataFrame([r._asdict() for r in results])
            
            # Format date and time columns
            try:
                df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            except:
                # If date is already a string or other format, leave it as is
                pass
                
            try:
                df['time'] = df['time'].astype(str)
            except:
                # If time is already a string or other format, leave it as is
                pass
            
            # Rename columns for better readability
            df = df.rename(columns={
                'id': 'ID',
                'date': 'Date',
                'time': 'Time',
                'status': 'Status',
                'course_name': 'Course',
                'professor_name': 'Professor',
                'group_name': 'Group',
                'room_name': 'Room'
            })
        
        # Create Excel file
        output = io.BytesIO()
        
        if format.lower() == "excel":
            # Create Excel writer
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Exam Schedule', index=False)
                
            # Set response headers
            response.headers["Content-Disposition"] = "attachment; filename=exam_schedule.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            # Return Excel file
            output.seek(0)
            return Response(content=output.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        elif format.lower() == "csv":
            # Convert to CSV
            csv_data = df.to_csv(index=False)
            
            # Set response headers
            response.headers["Content-Disposition"] = "attachment; filename=exam_schedule.csv"
            response.headers["Content-Type"] = "text/csv"
            
            # Return CSV file
            return Response(content=csv_data, media_type="text/csv")
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported format. Use 'excel' or 'csv'."
            )
    
    except Exception as e:
        # Log the error
        print(f"Error exporting exam schedule: {str(e)}")
        
        # Return a simple error message instead of an internal server error
        return {"error": "An error occurred while exporting the exam schedule.", "details": str(e)}
