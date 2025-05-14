"""
Script to clean the database and keep only data from orar.usv.ro links
This script handles the specific data format from orar.usv.ro
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

def clean_database_with_sql(external_data):
    """
    Clean the database using direct SQL queries with proper data handling
    """
    db = next(get_db())
    try:
        print("\nCleaning the database...")

        # Extract data with proper handling of None values
        professor_names = get_professor_names(external_data['professors'])
        room_names = get_room_names(external_data['rooms'])
        faculty_ids = get_faculty_ids(external_data['faculties'])
        group_names = get_group_names(external_data['subgroups'])

        print(f"Extracted {len(professor_names)} valid professor names")
        print(f"Extracted {len(room_names)} valid room names")
        print(f"Extracted {len(faculty_ids)} valid faculty IDs")
        print(f"Extracted {len(group_names)} valid group names")

        # Keep track of deleted records
        deleted_professors = 0
        deleted_rooms = 0
        deleted_groups = 0
        deleted_faculties = 0

        # Delete professors not from orar.usv.ro
        if professor_names:
            # Create a SQL string with all professor names, properly escaped
            professor_names_sql = "', '".join([name.replace("'", "''") for name in professor_names])
            if professor_names_sql:
                # Count professors to be deleted
                count_query = text(f"SELECT COUNT(*) FROM professors WHERE name NOT IN ('{professor_names_sql}')")
                deleted_professors = db.execute(count_query).scalar() or 0
                
                if deleted_professors > 0:
                    # Delete professors not in the list
                    delete_query = text(f"DELETE FROM professors WHERE name NOT IN ('{professor_names_sql}')")
                    db.execute(delete_query)
                    print(f"Deleted {deleted_professors} professors not from orar.usv.ro")
                else:
                    print("No professors to delete")

        # Delete rooms not from orar.usv.ro
        if room_names:
            room_names_sql = "', '".join([name.replace("'", "''") for name in room_names])
            if room_names_sql:
                # Count rooms to be deleted
                count_query = text(f"SELECT COUNT(*) FROM sala WHERE name NOT IN ('{room_names_sql}')")
                deleted_rooms = db.execute(count_query).scalar() or 0
                
                if deleted_rooms > 0:
                    # Delete rooms not in the list
                    delete_query = text(f"DELETE FROM sala WHERE name NOT IN ('{room_names_sql}')")
                    db.execute(delete_query)
                    print(f"Deleted {deleted_rooms} rooms not from orar.usv.ro")
                else:
                    print("No rooms to delete")

        # Delete groups not from orar.usv.ro
        if group_names:
            group_names_sql = "', '".join([name.replace("'", "''") for name in group_names])
            if group_names_sql:
                # Count groups to be deleted
                count_query = text(f"SELECT COUNT(*) FROM grupa WHERE name NOT IN ('{group_names_sql}')")
                deleted_groups = db.execute(count_query).scalar() or 0
                
                if deleted_groups > 0:
                    # Delete groups not in the list
                    delete_query = text(f"DELETE FROM grupa WHERE name NOT IN ('{group_names_sql}')")
                    db.execute(delete_query)
                    print(f"Deleted {deleted_groups} groups not from orar.usv.ro")
                else:
                    print("No groups to delete")

        # Delete faculties not from orar.usv.ro
        if faculty_ids:
            faculty_ids_sql = "', '".join([fid.replace("'", "''") for fid in faculty_ids])
            if faculty_ids_sql:
                # Count faculties to be deleted
                count_query = text(f"SELECT COUNT(*) FROM faculties WHERE id NOT IN ('{faculty_ids_sql}')")
                deleted_faculties = db.execute(count_query).scalar() or 0
                
                if deleted_faculties > 0:
                    # Delete faculties not in the list
                    delete_query = text(f"DELETE FROM faculties WHERE id NOT IN ('{faculty_ids_sql}')")
                    db.execute(delete_query)
                    print(f"Deleted {deleted_faculties} faculties not from orar.usv.ro")
                else:
                    print("No faculties to delete")

        # Commit changes
        db.commit()
        print("Database cleaned successfully!")

    except Exception as e:
        print(f"Error cleaning database: {e}")
        db.rollback()

async def main():
    print("Checking current database content...")
    check_database_content()

    # Fetch external data
    external_data = await fetch_external_data()

    # Clean database
    clean_database_with_sql(external_data)

    # Check database content after cleaning
    print("\nDatabase content after cleaning:")
    check_database_content()

if __name__ == "__main__":
    asyncio.run(main())
