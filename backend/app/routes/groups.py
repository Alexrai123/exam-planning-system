from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from ..db.base import get_db
from ..models.grupa import Grupa
from ..models.user import User, UserRole
from ..schemas.grupa import GrupaResponse, GrupaCreate, GrupaUpdate
from ..schemas.user import UserResponse
from ..routes.auth import get_current_user, is_secretariat

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("/", response_model=List[GrupaResponse])
def get_groups(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve groups. All authenticated users can access this endpoint.
    """
    groups = db.query(Grupa).offset(skip).limit(limit).all()
    return groups

@router.post("/", response_model=GrupaResponse)
def create_group(
    group_in: GrupaCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Create a new group. Only secretariat can access this endpoint.
    """
    # Check if group with this name already exists
    existing_group = db.query(Grupa).filter(Grupa.name == group_in.name).first()
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group with this name already exists"
        )
    
    group = Grupa(**group_in.dict())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@router.get("/{group_name}", response_model=GrupaResponse)
def get_group(
    group_name: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get a specific group by name. All authenticated users can access this endpoint.
    """
    group = db.query(Grupa).filter(Grupa.name == group_name).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    return group

@router.put("/{group_name}", response_model=GrupaResponse)
def update_group(
    group_name: str,
    group_in: GrupaUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Update a group. Only secretariat can access this endpoint.
    """
    group = db.query(Grupa).filter(Grupa.name == group_name).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    update_data = group_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)
    
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@router.put("/{group_name}/leader", response_model=GrupaResponse)
def assign_group_leader(
    group_name: str,
    leader_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Assign a leader to a group. Only secretariat can access this endpoint.
    """
    # Check if group exists
    group = db.query(Grupa).filter(Grupa.name == group_name).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Check if user exists and is a student
    user = db.query(User).filter(User.id == leader_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only students can be group leaders"
        )
    
    # Assign the leader
    group.leader_id = leader_id
    db.commit()
    db.refresh(group)
    return group

@router.delete("/{group_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_name: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> None:
    """
    Delete a group. Only secretariat can access this endpoint.
    """
    group = db.query(Grupa).filter(Grupa.name == group_name).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    db.delete(group)
    db.commit()
    return None
