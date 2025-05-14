from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, BackgroundTasks
from starlette.responses import Response
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from datetime import date, time
import sqlalchemy as sa

from ..db.base import get_db
from ..models.exam import Exam, ExamStatus
from ..models.course import Course
from ..models.sala import Sala
from ..models.grupa import Grupa
from ..models.user import User, UserRole
from ..schemas.exam import ExamResponse, ExamCreate, ExamUpdate, ExamStatusUpdate, ProfessorAgreementUpdate
from ..routes.auth import get_current_user, is_secretariat, is_professor, is_group_leader, is_student
from ..services.email import send_exam_notification, send_exam_agreement_notification
from ..services.excel import generate_exams_excel
from ..services.pdf import generate_exams_pdf

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.patch("/{exam_id}/agreement", response_model=ExamResponse)
async def update_professor_agreement(
    exam_id: int,
    agreement: ProfessorAgreementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_professor)
):
    """
    Update professor agreement status for an exam.
    Only professors can update their agreement status for exams related to their courses.
    """
    # Get the exam
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Get the course
    course = db.query(Course).filter(Course.id == exam.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if the professor is authorized to update this exam
    try:
        # Either they are the directly assigned professor or they are the course's professor
        is_assigned_professor = hasattr(exam, 'professor_id') and exam.professor_id == current_user.id
        is_course_professor = course.profesor_id == current_user.id
        
        if not (is_assigned_professor or is_course_professor):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update agreement status for exams where you are the assigned professor"
            )
    except Exception as e:
        # If professor_id field doesn't exist, fall back to checking only the course professor
        print(f"Note: professor_id field handling error in agreement: {str(e)}")
        if course.profesor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update agreement status for your courses"
            )
    
    # Update the agreement status
    exam.professor_agreement = agreement.professor_agreement
    
    # If professor agrees, update the status to confirmed
    if agreement.professor_agreement:
        exam.status = ExamStatus.CONFIRMED
    else:
        # If professor disagrees, keep the status as proposed
        # This allows the group leader to propose a new date
        exam.status = ExamStatus.PROPOSED
    
    db.commit()
    db.refresh(exam)
    
    # Send notification to group leader
    await send_exam_agreement_notification(exam, db, agreement.professor_agreement)
    
    return exam

@router.get("/", response_model=List[ExamResponse])
def get_exams(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    course_id: Optional[int] = None,
    grupa_name: Optional[str] = None,
    sala_id: Optional[int] = None,
    status: Optional[ExamStatus] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    response: Response = None
) -> Any:
    # Add CORS headers directly to this endpoint's response
    if response:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
    """
    Retrieve exams with optional filtering. All authenticated users can access this endpoint.
    """
    query = db.query(Exam)
    
    if course_id:
        query = query.filter(Exam.course_id == course_id)
    if grupa_name:
        query = query.filter(Exam.grupa_name == grupa_name)
    if sala_id:
        query = query.filter(Exam.sala_id == sala_id)
    if status:
        query = query.filter(Exam.status == status)
    if start_date:
        query = query.filter(Exam.date >= start_date)
    if end_date:
        query = query.filter(Exam.date <= end_date)
    
    exams = query.offset(skip).limit(limit).all()
    
    # Create a list of exam responses with professor_name
    exam_responses = []
    for exam in exams:
        # Create a dict from the exam model
        exam_dict = {
            "id": exam.id,
            "course_id": exam.course_id,
            "grupa_name": exam.grupa_name,
            "date": exam.date,
            "time": exam.time,
            "sala_name": exam.sala_name,
            "status": exam.status,
            "professor_agreement": exam.professor_agreement,
            "professor_name": None  # Default value
        }
        
        try:
            # Try to get the professor name from the directly assigned professor if the field exists
            if hasattr(exam, 'professor_id') and exam.professor_id:
                professor = db.query(User).filter(User.id == exam.professor_id).first()
                if professor:
                    exam_dict["professor_name"] = professor.name
                    
            # If no direct professor or professor name not found, try the course's professor
            if not exam_dict["professor_name"]:
                course = db.query(Course).filter(Course.id == exam.course_id).first()
                if course and course.profesor_id:
                    professor = db.query(User).filter(User.id == course.profesor_id).first()
                    if professor:
                        exam_dict["professor_name"] = professor.name
                        
            # If still no professor name, set to N/A
            if not exam_dict["professor_name"]:
                exam_dict["professor_name"] = "N/A"
                
        except Exception as e:
            # If there's an error getting the professor name, set to N/A
            print(f"Error getting professor name for exam {exam.id}: {str(e)}")
            exam_dict["professor_name"] = "N/A"
            
        exam_responses.append(exam_dict)
    
    return exam_responses

@router.post("/", response_model=ExamResponse)
def create_exam(
    exam_in: ExamCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Create a new exam. Secretariat can create confirmed exams, group leaders can propose exams.
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == exam_in.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if group exists
    grupa = db.query(Grupa).filter(Grupa.name == exam_in.grupa_name).first()
    if not grupa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if room exists
    sala = db.query(Sala).filter(Sala.name == exam_in.sala_name).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if room is available at the specified date and time
    room_availability = db.query(Exam).filter(
        Exam.sala_name == exam_in.sala_name,
        Exam.date == exam_in.date,
        Exam.time == exam_in.time
    ).first()
    
    if room_availability:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is already booked at the specified date and time"
        )
    
    # Check if group has another exam at the same date and time
    group_availability = db.query(Exam).filter(
        Exam.grupa_name == exam_in.grupa_name,
        Exam.date == exam_in.date,
        Exam.time == exam_in.time
    ).first()
    
    if group_availability:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group already has an exam at the specified date and time"
        )
    
    # Check user permissions and set appropriate status
    is_secretariat_user = current_user.role.upper() == UserRole.SECRETARIAT
    is_leader = False
    
    if not is_secretariat_user:
        # Check if user is a group leader for this specific group
        if current_user.role.upper() != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only secretariat or group leaders can create exams"
            )
        
        # Check if the user is the leader of the group specified in the exam
        if grupa.leader_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create exams for groups you lead"
            )
        
        is_leader = True
    
    # Create exam with appropriate status
    exam_data = exam_in.dict()
    if is_leader:
        # Group leaders can only propose exams
        exam_data["status"] = ExamStatus.PROPOSED
        # Set professor_agreement to False by default for proposed exams
        exam_data["professor_agreement"] = False
    elif is_secretariat_user and not exam_data.get("status"):
        # Secretariat creates confirmed exams by default
        exam_data["status"] = ExamStatus.CONFIRMED
        
    # Handle professor_id field if it exists in the database schema
    try:
        # If professor_id is provided, use it directly
        # Otherwise, try to get the professor from the course
        if not exam_data.get("professor_id"):
            course = db.query(Course).filter(Course.id == exam_data["course_id"]).first()
            if course and course.profesor_id:
                exam_data["professor_id"] = course.profesor_id
    except Exception as e:
        # If professor_id field doesn't exist in the database schema, remove it from the data
        print(f"Note: professor_id field handling error: {str(e)}")
        if "professor_id" in exam_data:
            del exam_data["professor_id"]
    
    exam = Exam(**exam_data)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    
    # Send notification email to professor
    try:
        send_exam_notification(exam, db)
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error sending email notification: {str(e)}")
    
    return exam

@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get a specific exam by id. All authenticated users can access this endpoint.
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    return exam

@router.put("/{exam_id}", response_model=ExamResponse)
def update_exam(
    exam_id: int,
    exam_in: ExamUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Update an exam. Secretariat can update all fields, professors can only update status.
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Check permissions
    is_admin = current_user.role == "secretariat"
    is_prof = current_user.role == "professor"
    
    # If user is professor, they can only update status
    if is_prof and not is_admin:
        # Get the course for this exam
        course = db.query(Course).filter(Course.id == exam.course_id).first()
        
        # Check if the professor is assigned to this course
        if course.profesor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update exams for your courses"
            )
        
        # Professor can only update status
        if exam_in.status:
            exam.status = exam_in.status
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Professors can only update exam status"
            )
    else:
        # Secretariat can update all fields
        update_data = exam_in.dict(exclude_unset=True)
        
        # If updating room, date or time, check availability
        if "sala_name" in update_data or "date" in update_data or "time" in update_data:
            sala_name = update_data.get("sala_name", exam.sala_name)
            date_val = update_data.get("date", exam.date)
            time_val = update_data.get("time", exam.time)
            
            # Check if room is available
            room_availability = db.query(Exam).filter(
                Exam.sala_name == sala_name,
                Exam.date == date_val,
                Exam.time == time_val,
                Exam.id != exam_id
            ).first()
            
            if room_availability:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Room is already booked at the specified date and time"
                )
            
            # Check if group has another exam
            grupa_id = update_data.get("grupa_name", exam.grupa_name)
            group_availability = db.query(Exam).filter(
                Exam.grupa_name == grupa_id,
                Exam.date == date_val,
                Exam.time == time_val,
                Exam.id != exam_id
            ).first()
            
            if group_availability:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Group already has an exam at the specified date and time"
                )
        
        # Handle professor_id specifically if it exists in the database schema
        try:
            if 'professor_id' in update_data and update_data['professor_id'] is not None:
                # If a professor_id is provided, use it directly
                exam.professor_id = update_data['professor_id']
            elif 'course_id' in update_data and update_data['course_id'] is not None:
                # If course_id is changed and no professor_id is provided, try to get the professor from the new course
                course = db.query(Course).filter(Course.id == update_data['course_id']).first()
                if course and course.profesor_id:
                    exam.professor_id = course.profesor_id
        except Exception as e:
            # If professor_id field doesn't exist in the database schema, remove it from the data
            print(f"Note: professor_id field handling error in update: {str(e)}")
            if 'professor_id' in update_data:
                del update_data['professor_id']
        
        # Update other fields
        for field, value in update_data.items():
            if field != 'professor_id':  # Skip professor_id as we've already handled it
                setattr(exam, field, value)
    
    db.add(exam)
    db.commit()
    db.refresh(exam)
    
    # Send notification if status changed to confirmed
    if exam_in.status == ExamStatus.CONFIRMED:
        try:
            send_exam_notification(exam, db, is_confirmation=True)
        except Exception as e:
            # Log the error but don't fail the request
            print(f"Error sending email notification: {str(e)}")
    
    return exam

@router.patch("/{exam_id}/status", response_model=ExamResponse)
def update_exam_status(
    exam_id: int,
    status_update: ExamStatusUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Update only the status of an exam. Secretariat can update to any status,
    professors can only update status for their own courses.
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Check permissions
    is_admin = current_user.role == "secretariat"
    is_prof = current_user.role == "professor"
    
    # If user is professor, check if they are assigned to this course
    if is_prof and not is_admin:
        # Get the course for this exam
        course = db.query(Course).filter(Course.id == exam.course_id).first()
        
        # Check if the professor is assigned to this course
        if course.profesor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update exams for your courses"
            )
    
    # Update the status
    exam.status = status_update.status
    
    # If status is being set to CONFIRMED, ensure professor_agreement is True
    if status_update.status == ExamStatus.CONFIRMED:
        exam.professor_agreement = True

    db.add(exam)
    db.commit()
    db.refresh(exam)
    
    # Send notification about status change
    try:
        send_exam_notification(
            exam=exam,
            action="status_update",
            db=db
        )
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Failed to send notification: {str(e)}")
    
    return exam

@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> None:
    """
    Delete an exam. Only secretariat can access this endpoint.
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    db.delete(exam)
    db.commit()
    return {"message": "Exam deleted successfully"}

@router.get("/export/excel", response_class=Response)
def export_exams_excel(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    course_id: Optional[int] = None,
    grupa_name: Optional[str] = None,
    sala_id: Optional[int] = None,
    status: Optional[ExamStatus] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Any:
    """
    Export exams to Excel format. All authenticated users can access this endpoint,
    but it's primarily intended for secretariat users.
    """
    # Build query with filters (similar to get_exams endpoint)
    query = db.query(Exam)
    
    if course_id:
        query = query.filter(Exam.course_id == course_id)
    if grupa_name:
        query = query.filter(Exam.grupa_name == grupa_name)
    if sala_id:
        query = query.filter(Exam.sala_id == sala_id)
    if status:
        query = query.filter(Exam.status == status)
    if start_date:
        query = query.filter(Exam.date >= start_date)
    if end_date:
        query = query.filter(Exam.date <= end_date)
    
    # If user is a professor, only show exams for their courses
    if current_user.role.upper() == UserRole.PROFESSOR:
        # Get courses taught by this professor
        professor_courses = db.query(Course).filter(
            Course.profesor_id == current_user.id
        ).all()
        professor_course_ids = [course.id for course in professor_courses]
        
        # Filter exams to only include those for the professor's courses
        query = query.filter(Exam.course_id.in_(professor_course_ids))
    
    exams = query.all()
    
    # Generate Excel file
    excel_data = generate_exams_excel(exams, db)
    
    # Set response headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename="exam_schedule.xlsx"',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    
    return Response(content=excel_data, headers=headers)

@router.get("/export/pdf", response_class=Response)
def export_exams_pdf(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    course_id: Optional[int] = None,
    grupa_name: Optional[str] = None,
    sala_id: Optional[int] = None,
    status: Optional[ExamStatus] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Any:
    """
    Export exams to PDF format. All authenticated users can access this endpoint,
    but it's primarily intended for secretariat users.
    """
    # Build query with filters (similar to get_exams endpoint)
    query = db.query(Exam)
    
    if course_id:
        query = query.filter(Exam.course_id == course_id)
    if grupa_name:
        query = query.filter(Exam.grupa_name == grupa_name)
    if sala_id:
        query = query.filter(Exam.sala_id == sala_id)
    if status:
        query = query.filter(Exam.status == status)
    if start_date:
        query = query.filter(Exam.date >= start_date)
    if end_date:
        query = query.filter(Exam.date <= end_date)
    
    # If user is a professor, only show exams for their courses
    if current_user.role.upper() == UserRole.PROFESSOR:
        # Get courses taught by this professor
        professor_courses = db.query(Course).filter(
            Course.profesor_id == current_user.id
        ).all()
        professor_course_ids = [course.id for course in professor_courses]
        
        # Filter exams to only include those for the professor's courses
        query = query.filter(Exam.course_id.in_(professor_course_ids))
    
    exams = query.all()
    
    # Generate PDF file
    pdf_data = generate_exams_pdf(exams, db)
    
    # Set response headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename="exam_schedule.pdf"',
        'Content-Type': 'application/pdf'
    }
    
    return Response(content=pdf_data, headers=headers)

@router.post("/auto-schedule", response_model=List[ExamResponse])
def auto_schedule_exams(
    course_ids: List[int] = Query(...),
    grupa_names: List[str] = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Automatically schedule exams for the given courses and groups.
    Only secretariat can access this endpoint.
    """
    from datetime import timedelta
    import random
    
    # Get all available rooms
    rooms = db.query(Sala).all()
    if not rooms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No rooms available for scheduling"
        )
    
    # Get all courses
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
    if len(courses) != len(course_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more courses not found"
        )
    
    # Get all groups
    groups = db.query(Grupa).filter(Grupa.name.in_(grupa_names)).all()
    if len(groups) != len(grupa_names):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more groups not found"
        )
    
    # Define possible exam times
    exam_times = [
        time(9, 0),  # 9:00 AM
        time(12, 0), # 12:00 PM
        time(15, 0)  # 3:00 PM
    ]
    
    # Create a list of all possible dates between start_date and end_date
    current_date = start_date
    available_dates = []
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:  # Monday to Friday
            available_dates.append(current_date)
        current_date += timedelta(days=1)
    
    if not available_dates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available dates in the specified range"
        )
    
    # Create exams
    created_exams = []
    
    for course in courses:
        for group in groups:
            # Try to find an available slot
            scheduled = False
            
            # Shuffle dates and times to get random distribution
            random.shuffle(available_dates)
            
            for exam_date in available_dates:
                random.shuffle(exam_times)
                
                for exam_time in exam_times:
                    random.shuffle(rooms)
                    
                    for room in rooms:
                        # Check if room is available at this date and time
                        room_availability = db.query(Exam).filter(
                            Exam.sala_name == room.name,
                            Exam.date == exam_date,
                            Exam.time == exam_time
                        ).first()
                        
                        if not room_availability:
                            # Check if group already has an exam at this date and time
                            group_availability = db.query(Exam).filter(
                                Exam.grupa_name == group.name,
                                Exam.date == exam_date,
                                Exam.time == exam_time
                            ).first()
                            
                            if not group_availability:
                                # Create exam
                                exam = Exam(
                                    course_id=course.id,
                                    grupa_name=group.name,
                                    date=exam_date,
                                    time=exam_time,
                                    sala_name=room.name,
                                    status=ExamStatus.PROPOSED
                                )
                                db.add(exam)
                                db.commit()
                                db.refresh(exam)
                                created_exams.append(exam)
                                
                                # Send notification email to professor
                                try:
                                    send_exam_notification(exam, db)
                                except Exception as e:
                                    # Log the error but don't fail the request
                                    print(f"Error sending email notification: {str(e)}")
                                
                                scheduled = True
                                break
                        
                        if scheduled:
                            break
                    
                    if scheduled:
                        break
                
                if scheduled:
                    break
            
            if not scheduled:
                # Could not schedule this exam
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Could not find available slot for course {course.name} and group {group.name}"
                )
    
    return created_exams
