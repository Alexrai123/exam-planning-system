"""
Script to clean the database and keep only data from orar.usv.ro links
This script uses direct SQL queries to avoid ORM relationship issues
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
from app.core.config import settings

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

def clean_database_with_sql(external_data):
    """
    Clean the database using direct SQL queries
    """
    db = next(get_db())
    try:
        print("\nCleaning the database...")

        # Extract IDs from external data
        professor_ids = [str(p.get('id')) for p in external_data['professors']]
        room_ids = [str(r.get('id')) for r in external_data['rooms']]
        faculty_ids = [str(f.get('id')) for f in external_data['faculties']]
        group_ids = [str(g.get('id')) for g in external_data['subgroups']]

        # Keep track of deleted records
        deleted_professors = 0
        deleted_rooms = 0
        deleted_groups = 0
        deleted_faculties = 0

        # Delete professors not from orar.usv.ro
        if professor_ids:
            # Convert list to comma-separated string for SQL IN clause
            professor_ids_str = ','.join(professor_ids)
            if professor_ids_str:
                # Count professors to be deleted
                count_query = text(f"SELECT COUNT(*) FROM professors WHERE id NOT IN ({professor_ids_str})")
                deleted_professors = db.execute(count_query).scalar() or 0
                
                # Delete professors not in the list
                delete_query = text(f"DELETE FROM professors WHERE id NOT IN ({professor_ids_str})")
                db.execute(delete_query)

        # Delete rooms not from orar.usv.ro
        if room_ids:
            room_ids_str = ','.join(room_ids)
            if room_ids_str:
                # Count rooms to be deleted
                count_query = text(f"SELECT COUNT(*) FROM sala WHERE id NOT IN ({room_ids_str})")
                deleted_rooms = db.execute(count_query).scalar() or 0
                
                # Delete rooms not in the list
                delete_query = text(f"DELETE FROM sala WHERE id NOT IN ({room_ids_str})")
                db.execute(delete_query)

        # Delete groups not from orar.usv.ro
        if group_ids:
            group_ids_str = ','.join(group_ids)
            if group_ids_str:
                # Count groups to be deleted
                count_query = text(f"SELECT COUNT(*) FROM grupa WHERE id NOT IN ({group_ids_str})")
                deleted_groups = db.execute(count_query).scalar() or 0
                
                # Delete groups not in the list
                delete_query = text(f"DELETE FROM grupa WHERE id NOT IN ({group_ids_str})")
                db.execute(delete_query)

        # Delete faculties not from orar.usv.ro
        if faculty_ids:
            faculty_ids_str = ','.join(faculty_ids)
            if faculty_ids_str:
                # Count faculties to be deleted
                count_query = text(f"SELECT COUNT(*) FROM faculties WHERE id NOT IN ({faculty_ids_str})")
                deleted_faculties = db.execute(count_query).scalar() or 0
                
                # Delete faculties not in the list
                delete_query = text(f"DELETE FROM faculties WHERE id NOT IN ({faculty_ids_str})")
                db.execute(delete_query)

        # Commit changes
        db.commit()

        print(f"Deleted {deleted_professors} professors not from orar.usv.ro")
        print(f"Deleted {deleted_rooms} rooms not from orar.usv.ro")
        print(f"Deleted {deleted_groups} groups not from orar.usv.ro")
        print(f"Deleted {deleted_faculties} faculties not from orar.usv.ro")
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
