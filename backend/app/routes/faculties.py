from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db.base import get_db
from ..models.faculty import Faculty
from ..schemas.faculty import FacultyResponse
from ..routes.auth import get_current_user

router = APIRouter(
    prefix="/faculties",
    tags=["faculties"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[FacultyResponse])
def get_faculties(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve all faculties.
    """
    faculties = db.query(Faculty).offset(skip).limit(limit).all()
    return faculties

@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty(
    faculty_id: str, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve a specific faculty by ID.
    """
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty
