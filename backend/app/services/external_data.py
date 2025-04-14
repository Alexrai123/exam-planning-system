import aiohttp
import asyncio
import logging
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URLs for external data
PROFESSORS_URL = "https://orar.usv.ro/orar/vizualizare/data/cadre.php?json"
ROOMS_URL = "https://orar.usv.ro/orar/vizualizare/data/sali.php?json"
FACULTIES_URL = "https://orar.usv.ro/orar/vizualizare/data/facultati.php?json"
SUBGROUPS_URL = "https://orar.usv.ro/orar/vizualizare/data/subgrupe.php?json"

async def fetch_json_data(url: str) -> List[Dict[str, Any]]:
    """
    Fetch JSON data from a given URL
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to fetch data from {url}. Status: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Error fetching data from {url}: {str(e)}")
        return []

async def get_professors() -> List[Dict[str, Any]]:
    """
    Fetch professors data from external API
    """
    professors = await fetch_json_data(PROFESSORS_URL)
    # Process professors data to match our model
    processed_professors = []
    for professor in professors:
        # Combine first and last name
        full_name = f"{professor.get('firstName', '')} {professor.get('lastName', '')}".strip()
        # Skip if no name
        if not full_name:
            continue
            
        processed_professors.append({
            "name": full_name,
            "specialization": professor.get('departmentName', ''),
            "title": "",  # Not provided in the external data
            "email": professor.get('emailAddress', ''),
            "phone": professor.get('phoneNumber', ''),
            "faculty": professor.get('facultyName', '')
        })
    return processed_professors

async def get_rooms() -> List[Dict[str, Any]]:
    """
    Fetch rooms data from external API
    """
    rooms = await fetch_json_data(ROOMS_URL)
    # Process rooms data to match our model
    processed_rooms = []
    for room in rooms:
        processed_rooms.append({
            "name": room.get('name', ''),
            "building": room.get('buildingName', ''),
            "capacity": int(room.get('capacitate', 0)) if room.get('capacitate', '').isdigit() else 0,
            "computers": int(room.get('computers', 0)) if room.get('computers', '').isdigit() else 0
        })
    return processed_rooms

async def get_faculties() -> List[Dict[str, Any]]:
    """
    Fetch faculties data from external API
    """
    faculties = await fetch_json_data(FACULTIES_URL)
    # Process faculties data
    processed_faculties = []
    for faculty in faculties:
        processed_faculties.append({
            "id": faculty.get('id', ''),
            "short_name": faculty.get('shortName', ''),
            "long_name": faculty.get('longName', '')
        })
    return processed_faculties

async def get_subgroups() -> List[Dict[str, Any]]:
    """
    Fetch subgroups data from external API
    """
    subgroups = await fetch_json_data(SUBGROUPS_URL)
    # Process subgroups data to match our group model
    processed_subgroups = []
    for subgroup in subgroups:
        # Create a name that combines year, group name and subgroup index
        name = f"{subgroup.get('studyYear', '')}{subgroup.get('groupName', '')}{subgroup.get('subgroupIndex', '')}"
        processed_subgroups.append({
            "name": name,
            "year": int(subgroup.get('studyYear', 0)) if subgroup.get('studyYear', '').isdigit() else 0,
            "specialization": subgroup.get('specializationShortName', ''),
            "faculty_id": subgroup.get('facultyId', '')
        })
    return processed_subgroups

async def fetch_all_external_data():
    """
    Fetch all external data concurrently
    """
    professors_task = asyncio.create_task(get_professors())
    rooms_task = asyncio.create_task(get_rooms())
    faculties_task = asyncio.create_task(get_faculties())
    subgroups_task = asyncio.create_task(get_subgroups())
    
    professors = await professors_task
    rooms = await rooms_task
    faculties = await faculties_task
    subgroups = await subgroups_task
    
    return {
        "professors": professors,
        "rooms": rooms,
        "faculties": faculties,
        "subgroups": subgroups
    }
