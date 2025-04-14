import asyncio
import aiohttp
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.professor import Professor
from app.models.sala import Sala
from app.models.grupa import Grupa
from app.models.course import Course
from app.models.user import User
from app.db.base import Base
from app.core.config import settings

# URLs for external data
PROFESSORS_URL = "https://orar.usv.ro/orar/vizualizare/data/cadre.php?json"
ROOMS_URL = "https://orar.usv.ro/orar/vizualizare/data/sali.php?json"
FACULTIES_URL = "https://orar.usv.ro/orar/vizualizare/data/facultati.php?json"
SUBGROUPS_URL = "https://orar.usv.ro/orar/vizualizare/data/subgrupe.php?json"

# Create database engine and session
engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

async def fetch_json_data(url):
    """
    Fetch JSON data from a given URL
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to fetch data from {url}. Status: {response.status}")
                    return []
    except Exception as e:
        print(f"Error fetching data from {url}: {str(e)}")
        return []

async def process_professors():
    """
    Fetch and process professors data
    """
    print("Importing professors...")
    professors_data = await fetch_json_data(PROFESSORS_URL)
    
    imported_count = 0
    updated_count = 0
    
    for professor in professors_data:
        # Combine first and last name
        full_name = f"{professor.get('firstName', '')} {professor.get('lastName', '')}".strip()
        
        # Skip if no name
        if not full_name:
            continue
            
        # Check if professor already exists
        existing_professor = db.query(Professor).filter(
            Professor.name == full_name
        ).first()
        
        if existing_professor:
            # Update existing professor
            existing_professor.specialization = professor.get('departmentName', '')
            existing_professor.email = professor.get('emailAddress', '')
            existing_professor.phone = professor.get('phoneNumber', '')
            existing_professor.faculty = professor.get('facultyName', '')
            updated_count += 1
        else:
            # Create new professor
            new_professor = Professor(
                name=full_name,
                specialization=professor.get('departmentName', ''),
                title="",  # Not provided in the external data
                email=professor.get('emailAddress', ''),
                phone=professor.get('phoneNumber', ''),
                faculty=professor.get('facultyName', '')
            )
            db.add(new_professor)
            imported_count += 1
    
    db.commit()
    print(f"Professors imported: {imported_count} new, {updated_count} updated")
    return imported_count, updated_count

async def process_rooms():
    """
    Fetch and process rooms data
    """
    print("Importing rooms...")
    rooms_data = await fetch_json_data(ROOMS_URL)
    
    imported_count = 0
    updated_count = 0
    
    for room in rooms_data:
        room_name = room.get('name', '')
        
        # Skip if no name
        if not room_name:
            continue
            
        # Check if room already exists
        existing_room = db.query(Sala).filter(
            Sala.name == room_name
        ).first()
        
        # Convert capacity and computers to integers
        capacity = int(room.get('capacitate', 0)) if room.get('capacitate', '').isdigit() else 0
        computers = int(room.get('computers', 0)) if room.get('computers', '').isdigit() else 0
        
        if existing_room:
            # Update existing room
            existing_room.building = room.get('buildingName', '')
            existing_room.capacity = capacity
            existing_room.computers = computers
            updated_count += 1
        else:
            # Create new room
            new_room = Sala(
                name=room_name,
                building=room.get('buildingName', ''),
                capacity=capacity,
                computers=computers
            )
            db.add(new_room)
            imported_count += 1
    
    db.commit()
    print(f"Rooms imported: {imported_count} new, {updated_count} updated")
    return imported_count, updated_count

async def process_groups():
    """
    Fetch and process subgroups data
    """
    print("Importing groups...")
    subgroups_data = await fetch_json_data(SUBGROUPS_URL)
    
    imported_count = 0
    updated_count = 0
    
    for subgroup in subgroups_data:
        # Create a name that combines year, group name and subgroup index
        name = f"{subgroup.get('studyYear', '')}{subgroup.get('groupName', '')}{subgroup.get('subgroupIndex', '')}"
        
        # Skip if no name
        if not name:
            continue
            
        # Check if group already exists
        existing_group = db.query(Grupa).filter(
            Grupa.name == name
        ).first()
        
        # Convert year to integer
        year = int(subgroup.get('studyYear', 0)) if subgroup.get('studyYear', '').isdigit() else 0
        
        if existing_group:
            # Update existing group
            existing_group.year = year
            existing_group.specialization = subgroup.get('specializationShortName', '')
            updated_count += 1
        else:
            # Create new group
            new_group = Grupa(
                name=name,
                year=year,
                specialization=subgroup.get('specializationShortName', '')
            )
            db.add(new_group)
            imported_count += 1
    
    db.commit()
    print(f"Groups imported: {imported_count} new, {updated_count} updated")
    return imported_count, updated_count

async def main():
    """
    Main function to import all data
    """
    print("Starting data import...")
    
    # Import professors
    professors_imported, professors_updated = await process_professors()
    
    # Import rooms
    rooms_imported, rooms_updated = await process_rooms()
    
    # Import groups
    groups_imported, groups_updated = await process_groups()
    
    print("\nImport completed!")
    print(f"Professors: {professors_imported} new, {professors_updated} updated")
    print(f"Rooms: {rooms_imported} new, {rooms_updated} updated")
    print(f"Groups: {groups_imported} new, {groups_updated} updated")
    
    # Close the database session
    db.close()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
