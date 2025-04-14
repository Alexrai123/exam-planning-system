from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from ..db.base import get_db
from ..models.professor import Professor
from ..models.user import User
from ..schemas.professor import ProfessorResponse, ProfessorCreate, ProfessorUpdate
from ..routes.auth import get_current_user, is_secretariat

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.get("/", response_model=List[ProfessorResponse])
def get_professors(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve professors. All authenticated users can access this endpoint.
    """
    professors = db.query(Professor).offset(skip).limit(limit).all()
    return professors

@router.post("/", response_model=ProfessorResponse)
def create_professor(
    professor_in: ProfessorCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Create a new professor profile. Only secretariat can access this endpoint.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == professor_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if professor profile already exists for this user
    existing_professor = db.query(Professor).filter(Professor.user_id == professor_in.user_id).first()
    if existing_professor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Professor profile already exists for this user"
        )
    
    professor = Professor(**professor_in.dict())
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor

@router.get("/{professor_id}", response_model=ProfessorResponse)
def get_professor(
    professor_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get a specific professor by id. All authenticated users can access this endpoint.
    """
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    return professor

@router.put("/{professor_id}", response_model=ProfessorResponse)
def update_professor(
    professor_id: int,
    professor_in: ProfessorUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Update a professor. Only secretariat can access this endpoint.
    """
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    update_data = professor_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(professor, field, value)
    
    db.commit()
    db.refresh(professor)
    return professor

@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professor(
    professor_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> None:
    """
    Delete a professor. Only secretariat can access this endpoint.
    """
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    db.delete(professor)
    db.commit()
    return None
