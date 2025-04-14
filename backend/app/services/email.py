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

def send_exam_notification(exam: Exam, db: Session, is_confirmation: bool = False):
    """
    Send an email notification about an exam to the professor
    """
    # Get related data
    course = db.query(Course).filter(Course.id == exam.course_id).first()
    professor = db.query(User).filter(User.id == course.profesor_id).first()
    group = db.query(Grupa).filter(Grupa.id == exam.grupa_id).first()
    room = db.query(Sala).filter(Sala.id == exam.sala_id).first()
    
    # Format date and time
    exam_date = exam.date.strftime("%d-%m-%Y")
    exam_time = exam.time.strftime("%H:%M")
    
    # Create email subject
    if is_confirmation:
        subject = f"Exam Confirmed: {course.name} on {exam_date}"
    else:
        subject = f"New Exam Scheduled: {course.name} on {exam_date}"
    
    # Create email body
    body = f"""
    <html>
    <body>
        <h2>{'Exam Confirmation' if is_confirmation else 'New Exam Scheduled'}</h2>
        <p>Dear {professor.name},</p>
        
        <p>{'An exam has been confirmed' if is_confirmation else 'A new exam has been scheduled'} with the following details:</p>
        
        <ul>
            <li><strong>Course:</strong> {course.name}</li>
            <li><strong>Date:</strong> {exam_date}</li>
            <li><strong>Time:</strong> {exam_time}</li>
            <li><strong>Group:</strong> {group.name}</li>
            <li><strong>Room:</strong> {room.name}</li>
            <li><strong>Status:</strong> {exam.status}</li>
        </ul>
        
        <p>{'Please make necessary preparations for the exam.' if is_confirmation else 'Please log in to the system to confirm or request changes to this exam.'}</p>
        
        <p>Best regards,<br>
        Exam Planning System</p>
    </body>
    </html>
    """
    
    # Send email asynchronously
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(send_email([professor.email], subject, body))
    finally:
        loop.close()
