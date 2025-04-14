from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from ..db.base import get_db
from ..models.course import Course
from ..schemas.course import CourseResponse, CourseCreate, CourseUpdate
from ..routes.auth import get_current_user, is_secretariat, is_professor

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve courses. All authenticated users can access this endpoint.
    """
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.post("/", response_model=CourseResponse)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Create a new course. Only secretariat can access this endpoint.
    """
    course = Course(**course_in.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get a specific course by id. All authenticated users can access this endpoint.
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_in: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Update a course. Only secretariat can access this endpoint.
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    update_data = course_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> None:
    """
    Delete a course. Only secretariat can access this endpoint.
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    db.delete(course)
    db.commit()
    return None
