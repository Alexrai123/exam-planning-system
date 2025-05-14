from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models.exam import Exam
from ..models.course import Course
from ..models.user import User
from ..models.grupa import Grupa
from ..models.sala import Sala
from typing import List
from datetime import datetime

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_USE_TLS,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(email_to: List[str], subject: str, body: str):
    """
    Send an email using FastMail
    """
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        body=body,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)


def send_exam_notification(exam: Exam, db: Session, is_confirmation=False):
    """Send notification to professor about a new exam"""
    try:
        # Get course details
        course = db.query(Course).filter(Course.id == exam.course_id).first()
        if not course:
            print(f"Course not found for exam ID {exam.id}")
            return
        
        # First try to get the professor directly assigned to the exam if the field exists
        try:
            if hasattr(exam, 'professor_id') and exam.professor_id:
                professor = db.query(User).filter(User.id == exam.professor_id).first()
            else:
                # Fall back to the course's professor if no direct assignment
                professor = db.query(User).filter(User.id == course.profesor_id).first()
        except Exception as e:
            # If professor_id field doesn't exist, fall back to the course's professor
            print(f"Note: professor_id field handling error in email notification: {str(e)}")
            professor = db.query(User).filter(User.id == course.profesor_id).first()
            
        if not professor or not professor.email:
            print(f"Professor not found or has no email for exam ID {exam.id}")
            return
            
        # Get group details
        group = db.query(Grupa).filter(Grupa.name == exam.grupa_name).first()
        group_name = group.name if group else exam.grupa_name
        
        # Get room details
        room = db.query(Sala).filter(Sala.name == exam.sala_name).first()
        room_name = room.name if room else exam.sala_name
        
        # Prepare email content
        subject = f"New Exam Proposed: {course.name}"
        body = f"""
        <html>
        <body>
            <h2>New Exam Proposed</h2>
            <p>Dear {professor.name},</p>
            
            <p>A new exam has been scheduled for your course '{course.name}'.</p>
            <p>Details:</p>
            <ul>
                <li><strong>Date:</strong> {exam.date.strftime('%d-%m-%Y')}</li>
                <li><strong>Time:</strong> {exam.time.strftime('%H:%M')}</li>
                <li><strong>Group:</strong> {group_name}</li>
                <li><strong>Room:</strong> {room_name}</li>
                <li><strong>Status:</strong> {exam.status}</li>
            </ul>
            
            <p>Please log in to the Exam Planning System to review and approve this exam.</p>
            
            <p>Thank you,<br>
            Exam Planning System</p>
        </body>
        </html>
        """
        
        # Skip email sending in development environment
        print(f"Email notification would be sent to {professor.email} for exam ID {exam.id}, course {course.name}")
        print(f"Email sending is disabled in development environment")
        return
        
    except Exception as e:
        print(f"Error sending email notification: {str(e)}")
        # Don't raise the exception to avoid disrupting the main flow


def send_exam_agreement_notification(exam: Exam, db: Session, is_agreed: bool = None):
    """Send notification to group leader about professor's decision on a proposed exam"""
    try:
        # Get course details
        course = db.query(Course).filter(Course.id == exam.course_id).first()
        if not course:
            print(f"Course not found for exam ID {exam.id}")
            return
        
        # Get group details and group leader
        group = db.query(Grupa).filter(Grupa.name == exam.grupa_name).first()
        if not group or not group.leader_id:
            print(f"Group not found or has no leader for exam ID {exam.id}")
            return
            
        # Get group leader details
        group_leader = db.query(User).filter(User.id == group.leader_id).first()
        if not group_leader or not group_leader.email:
            print(f"Group leader not found or has no email for group {group.name}")
            return
            
        # Get professor details - first try directly assigned professor, then fall back to course professor
        try:
            if hasattr(exam, 'professor_id') and exam.professor_id:
                professor = db.query(User).filter(User.id == exam.professor_id).first()
            else:
                professor = db.query(User).filter(User.id == course.profesor_id).first()
        except Exception as e:
            # If professor_id field doesn't exist, fall back to the course's professor
            print(f"Note: professor_id field handling error in agreement notification: {str(e)}")
            professor = db.query(User).filter(User.id == course.profesor_id).first()
            
        professor_name = professor.name if professor else "The professor"
        
        # Get room details
        room = db.query(Sala).filter(Sala.name == exam.sala_name).first()
        room_name = room.name if room else exam.sala_name
        
        # Determine the agreement status message
        agreement_status = "approved" if is_agreed else "rejected"
        
        # Prepare email content
        subject = f"Exam {agreement_status.capitalize()}: {course.name}"
        body = f"""
        <html>
        <body>
            <h2>Exam {agreement_status.capitalize()}</h2>
            <p>Dear {group_leader.name},</p>
            
            <p>The professor has {agreement_status} the exam for course '{course.name}'.</p>
            <p>Details:</p>
            <ul>
                <li><strong>Date:</strong> {exam.date.strftime('%d-%m-%Y')}</li>
                <li><strong>Time:</strong> {exam.time.strftime('%H:%M')}</li>
                <li><strong>Group:</strong> {group.name}</li>
                <li><strong>Room:</strong> {room_name}</li>
                <li><strong>Status:</strong> {exam.status}</li>
            </ul>
            
            <p>Please log in to the Exam Planning System for more details.</p>
            
            <p>Thank you,<br>
            Exam Planning System</p>
        </body>
        </html>
        """
        
        # Skip email sending in development environment
        print(f"Agreement notification would be sent to {group_leader.email} for exam ID {exam.id}, course {course.name}")
        print(f"Email sending is disabled in development environment")
        return
    except Exception as e:
        print(f"Error sending agreement notification: {str(e)}")
        # Don't raise the exception to avoid disrupting the main flow


# This function has been replaced with the improved version above
