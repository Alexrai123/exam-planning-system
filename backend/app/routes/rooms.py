from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from ..db.base import get_db
from ..models.sala import Sala
from ..schemas.sala import SalaResponse, SalaCreate, SalaUpdate
from ..routes.auth import get_current_user, is_secretariat

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=List[SalaResponse])
def get_rooms(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve rooms. All authenticated users can access this endpoint.
    """
    rooms = db.query(Sala).offset(skip).limit(limit).all()
    return rooms

@router.post("/", response_model=SalaResponse)
def create_room(
    room_in: SalaCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Create a new room. Only secretariat can access this endpoint.
    """
    room = Sala(**room_in.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("/{room_id}", response_model=SalaResponse)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get a specific room by id. All authenticated users can access this endpoint.
    """
    room = db.query(Sala).filter(Sala.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    return room

@router.put("/{room_id}", response_model=SalaResponse)
def update_room(
    room_id: int,
    room_in: SalaUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> Any:
    """
    Update a room. Only secretariat can access this endpoint.
    """
    room = db.query(Sala).filter(Sala.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    update_data = room_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)
    
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: Any = Depends(is_secretariat)
) -> None:
    """
    Delete a room. Only secretariat can access this endpoint.
    """
    room = db.query(Sala).filter(Sala.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    db.delete(room)
    db.commit()
    return None
