from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Any
import asyncio

from ..db.base import get_db
from ..routes.auth import get_current_active_user
from ..models.user import User
from ..models.professor import Professor
from ..models.sala import Sala
from ..models.grupa import Grupa
from ..services.external_data import (
    get_professors, 
    get_rooms, 
    get_faculties, 
    get_subgroups,
    fetch_all_external_data
)

router = APIRouter()

@router.get("/fetch", response_model=Dict[str, List[Dict[str, Any]]])
async def fetch_external_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Fetch all external data from the university API
    """
    # Only allow secretariat users to fetch external data
    if current_user.role != "secretariat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to fetch external data"
        )
    
    # Fetch all external data
    data = await fetch_all_external_data()
    return data

@router.post("/import/professors", response_model=Dict[str, Any])
async def import_professors(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import professors from external API to the database
    """
    # Only allow secretariat users to import data
    if current_user.role != "secretariat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to import data"
        )
    
    # Fetch professors data
    professors_data = await get_professors()
    
    # Import professors to database
    imported_count = 0
    skipped_count = 0
    
    for professor_data in professors_data:
        # Check if professor already exists
        existing_professor = db.query(Professor).filter(
            Professor.name == professor_data["name"]
        ).first()
        
        if existing_professor:
            # Update existing professor
            existing_professor.specialization = professor_data["specialization"]
            existing_professor.email = professor_data["email"]
            existing_professor.phone = professor_data["phone"]
            existing_professor.faculty = professor_data["faculty"]
            skipped_count += 1
        else:
            # Create new professor
            new_professor = Professor(
                name=professor_data["name"],
                specialization=professor_data["specialization"],
                title=professor_data["title"],
                email=professor_data["email"],
                phone=professor_data["phone"],
                faculty=professor_data["faculty"]
            )
            db.add(new_professor)
            imported_count += 1
    
    db.commit()
    
    return {
        "message": f"Successfully imported {imported_count} professors, updated {skipped_count} existing professors",
        "imported_count": imported_count,
        "updated_count": skipped_count,
        "total_count": len(professors_data)
    }

@router.post("/import/rooms", response_model=Dict[str, Any])
async def import_rooms(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import rooms from external API to the database
    """
    # Only allow secretariat users to import data
    if current_user.role != "secretariat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to import data"
        )
    
    # Fetch rooms data
    rooms_data = await get_rooms()
    
    # Import rooms to database
    imported_count = 0
    skipped_count = 0
    
    for room_data in rooms_data:
        # Skip rooms with empty names
        if not room_data["name"]:
            continue
            
        # Check if room already exists
        existing_room = db.query(Sala).filter(
            Sala.name == room_data["name"]
        ).first()
        
        if existing_room:
            # Update existing room
            existing_room.building = room_data["building"]
            existing_room.capacity = room_data["capacity"]
            existing_room.computers = room_data["computers"]
            skipped_count += 1
        else:
            # Create new room
            new_room = Sala(
                name=room_data["name"],
                building=room_data["building"],
                capacity=room_data["capacity"],
                computers=room_data["computers"]
            )
            db.add(new_room)
            imported_count += 1
    
    db.commit()
    
    return {
        "message": f"Successfully imported {imported_count} rooms, updated {skipped_count} existing rooms",
        "imported_count": imported_count,
        "updated_count": skipped_count,
        "total_count": len(rooms_data)
    }

@router.post("/import/groups", response_model=Dict[str, Any])
async def import_groups(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import groups from external API to the database
    """
    # Only allow secretariat users to import data
    if current_user.role != "secretariat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to import data"
        )
    
    # Fetch subgroups data
    subgroups_data = await get_subgroups()
    
    # Import groups to database
    imported_count = 0
    skipped_count = 0
    
    for group_data in subgroups_data:
        # Skip groups with empty names
        if not group_data["name"]:
            continue
            
        # Check if group already exists
        existing_group = db.query(Grupa).filter(
            Grupa.name == group_data["name"]
        ).first()
        
        if existing_group:
            # Update existing group
            existing_group.year = group_data["year"]
            existing_group.specialization = group_data["specialization"]
            skipped_count += 1
        else:
            # Create new group
            new_group = Grupa(
                name=group_data["name"],
                year=group_data["year"],
                specialization=group_data["specialization"]
            )
            db.add(new_group)
            imported_count += 1
    
    db.commit()
    
    return {
        "message": f"Successfully imported {imported_count} groups, updated {skipped_count} existing groups",
        "imported_count": imported_count,
        "updated_count": skipped_count,
        "total_count": len(subgroups_data)
    }

@router.post("/import/all", response_model=Dict[str, Any])
async def import_all_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import all data from external API to the database
    """
    # Only allow secretariat users to import data
    if current_user.role != "secretariat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to import data"
        )
    
    # Import professors
    professors_result = await import_professors(current_user, db)
    
    # Import rooms
    rooms_result = await import_rooms(current_user, db)
    
    # Import groups
    groups_result = await import_groups(current_user, db)
    
    return {
        "message": "Successfully imported all data",
        "professors": professors_result,
        "rooms": rooms_result,
        "groups": groups_result
    }
