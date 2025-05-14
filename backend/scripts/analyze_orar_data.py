"""
Script to analyze data from orar.usv.ro and compare with local database
"""
import sys
import os
from pathlib import Path
import asyncio
import aiohttp
import json

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db

# URLs for external data
PROFESSORS_URL = "https://orar.usv.ro/orar/vizualizare/data/cadre.php?json"
ROOMS_URL = "https://orar.usv.ro/orar/vizualizare/data/sali.php?json"
FACULTIES_URL = "https://orar.usv.ro/orar/vizualizare/data/facultati.php?json"
SUBGROUPS_URL = "https://orar.usv.ro/orar/vizualizare/data/subgrupe.php?json"

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

def check_database_content():
    """
    Check the current content of the database
    """
    db = next(get_db())
    try:
        # Check professors
        professors_query = text("SELECT COUNT(*) FROM professors")
        professors_count = db.execute(professors_query).scalar()
        print(f"Current professors count: {professors_count}")

        # Check rooms
        rooms_query = text("SELECT COUNT(*) FROM sala")
        rooms_count = db.execute(rooms_query).scalar()
        print(f"Current rooms count: {rooms_count}")

        # Check groups
        groups_query = text("SELECT COUNT(*) FROM grupa")
        groups_count = db.execute(groups_query).scalar()
        print(f"Current groups count: {groups_count}")

        # Check faculties
        faculties_query = text("SELECT COUNT(*) FROM faculties")
        faculties_count = db.execute(faculties_query).scalar()
        print(f"Current faculties count: {faculties_count}")

        # Check courses
        courses_query = text("SELECT COUNT(*) FROM courses")
        courses_count = db.execute(courses_query).scalar()
        print(f"Current courses count: {courses_count}")

        # Check exams
        exams_query = text("SELECT COUNT(*) FROM exams")
        exams_count = db.execute(exams_query).scalar()
        print(f"Current exams count: {exams_count}")

    except Exception as e:
        print(f"Error checking database content: {e}")

async def fetch_external_data():
    """
    Fetch all external data from orar.usv.ro
    """
    print("Fetching external data from orar.usv.ro...")

    # Fetch data concurrently
    professors_task = fetch_json_data(PROFESSORS_URL)
    rooms_task = fetch_json_data(ROOMS_URL)
    faculties_task = fetch_json_data(FACULTIES_URL)
    subgroups_task = fetch_json_data(SUBGROUPS_URL)

    professors_data = await professors_task
    rooms_data = await rooms_task
    faculties_data = await faculties_task
    subgroups_data = await subgroups_task

    print(f"Fetched {len(professors_data)} professors")
    print(f"Fetched {len(rooms_data)} rooms")
    print(f"Fetched {len(faculties_data)} faculties")
    print(f"Fetched {len(subgroups_data)} subgroups")

    return {
        'professors': professors_data,
        'rooms': rooms_data,
        'faculties': faculties_data,
        'subgroups': subgroups_data
    }

def get_professor_names(professors_data):
    """
    Extract professor names from the API data, handling None values
    """
    professor_names = []
    for p in professors_data:
        first_name = p.get('firstName', '') or ''
        last_name = p.get('lastName', '') or ''
        full_name = f"{first_name} {last_name}".strip()
        if full_name:  # Only add non-empty names
            professor_names.append(full_name)
    return professor_names

def get_room_names(rooms_data):
    """
    Extract room names from the API data, handling None values
    """
    room_names = []
    for r in rooms_data:
        name = r.get('name', '') or ''
        if name:  # Only add non-empty names
            room_names.append(name)
    return room_names

def get_faculty_ids(faculties_data):
    """
    Extract faculty IDs from the API data
    """
    faculty_ids = []
    for f in faculties_data:
        fid = f.get('id', '')
        if fid:  # Only add non-empty IDs
            faculty_ids.append(str(fid))
    return faculty_ids

def get_group_names(subgroups_data):
    """
    Extract group names from the API data, handling None values
    """
    group_names = []
    for g in subgroups_data:
        name = g.get('groupName', '') or ''
        if name:  # Only add non-empty names
            group_names.append(name)
    return group_names

def analyze_database_differences(external_data):
    """
    Analyze differences between external data and local database
    """
    db = next(get_db())
    try:
        print("\nAnalyzing differences between external data and local database...")

        # Extract data with proper handling of None values
        professor_names = get_professor_names(external_data['professors'])
        room_names = get_room_names(external_data['rooms'])
        faculty_ids = get_faculty_ids(external_data['faculties'])
        group_names = get_group_names(external_data['subgroups'])

        print(f"Extracted {len(professor_names)} valid professor names")
        print(f"Extracted {len(room_names)} valid room names")
        print(f"Extracted {len(faculty_ids)} valid faculty IDs")
        print(f"Extracted {len(group_names)} valid group names")

        # Get local data
        local_professors = db.execute(text("SELECT name FROM professors")).fetchall()
        local_professor_names = [p[0] for p in local_professors]
        
        local_rooms = db.execute(text("SELECT name FROM sala")).fetchall()
        local_room_names = [r[0] for r in local_rooms]
        
        local_faculties = db.execute(text("SELECT id FROM faculties")).fetchall()
        local_faculty_ids = [f[0] for f in local_faculties]
        
        local_groups = db.execute(text("SELECT name FROM grupa")).fetchall()
        local_group_names = [g[0] for g in local_groups]

        # Find differences
        professors_not_in_external = set(local_professor_names) - set(professor_names)
        rooms_not_in_external = set(local_room_names) - set(room_names)
        faculties_not_in_external = set(local_faculty_ids) - set(faculty_ids)
        groups_not_in_external = set(local_group_names) - set(group_names)

        # Print differences
        print(f"\nProfessors in local database but not in external data: {len(professors_not_in_external)}")
        if professors_not_in_external:
            print("Sample of professors to be removed:")
            for name in list(professors_not_in_external)[:10]:  # Show only first 10
                print(f"  - {name}")
            if len(professors_not_in_external) > 10:
                print(f"  ... and {len(professors_not_in_external) - 10} more")

        print(f"\nRooms in local database but not in external data: {len(rooms_not_in_external)}")
        if rooms_not_in_external:
            print("Sample of rooms to be removed:")
            for name in list(rooms_not_in_external)[:10]:
                print(f"  - {name}")
            if len(rooms_not_in_external) > 10:
                print(f"  ... and {len(rooms_not_in_external) - 10} more")

        print(f"\nFaculties in local database but not in external data: {len(faculties_not_in_external)}")
        if faculties_not_in_external:
            print("Sample of faculties to be removed:")
            for fid in list(faculties_not_in_external)[:10]:
                print(f"  - {fid}")
            if len(faculties_not_in_external) > 10:
                print(f"  ... and {len(faculties_not_in_external) - 10} more")

        print(f"\nGroups in local database but not in external data: {len(groups_not_in_external)}")
        if groups_not_in_external:
            print("Sample of groups to be removed:")
            for name in list(groups_not_in_external)[:10]:
                print(f"  - {name}")
            if len(groups_not_in_external) > 10:
                print(f"  ... and {len(groups_not_in_external) - 10} more")

    except Exception as e:
        print(f"Error analyzing database differences: {e}")

async def main():
    print("Checking current database content...")
    check_database_content()

    # Fetch external data
    external_data = await fetch_external_data()

    # Analyze differences
    analyze_database_differences(external_data)

if __name__ == "__main__":
    asyncio.run(main())
