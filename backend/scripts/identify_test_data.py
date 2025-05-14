"""
Script to identify test data in the database
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

def identify_test_professors():
    """
    Identify test professors in the database
    """
    db = next(get_db())
    try:
        # Get professors that are referenced in courses
        referenced_query = text("""
            SELECT DISTINCT p.name, COUNT(c.id) as course_count
            FROM professors p
            JOIN courses c ON p.name = c.profesor_name
            GROUP BY p.name
        """)
        referenced_professors = db.execute(referenced_query).fetchall()
        
        print("\nProfessors referenced in courses:")
        for prof in referenced_professors:
            print(f"  - {prof[0]} (referenced in {prof[1]} courses)")
        
        # Get professors with test-like names
        test_query = text("""
            SELECT name
            FROM professors
            WHERE name LIKE '%test%' OR name LIKE '%Test%' OR name = 'John Smith' OR name = 'None None'
        """)
        test_professors = db.execute(test_query).fetchall()
        
        print("\nProfessors with test-like names:")
        for prof in test_professors:
            print(f"  - {prof[0]}")
        
    except Exception as e:
        print(f"Error identifying test professors: {e}")

async def analyze_test_data():
    """
    Analyze test data in the database
    """
    print("Checking current database content...")
    check_database_content()
    
    # Identify test professors
    identify_test_professors()
    
    # Fetch external data
    print("\nFetching external data from orar.usv.ro...")
    
    # Fetch data concurrently
    professors_task = fetch_json_data(PROFESSORS_URL)
    
    professors_data = await professors_task
    
    print(f"Fetched {len(professors_data)} professors")
    
    # Extract professor names
    professor_names = get_professor_names(professors_data)
    print(f"Extracted {len(professor_names)} valid professor names")
    
    # Find professors not in external data
    db = next(get_db())
    local_professors = db.execute(text("SELECT name FROM professors")).fetchall()
    local_professor_names = [p[0] for p in local_professors]
    
    professors_not_in_external = set(local_professor_names) - set(professor_names)
    
    print(f"\nProfessors in local database but not in external data: {len(professors_not_in_external)}")
    if professors_not_in_external:
        print("List of professors not in external data:")
        for name in sorted(professors_not_in_external):
            # Check if this professor is referenced in courses
            escaped_name = name.replace("'", "''")
            ref_query = text(f"SELECT COUNT(*) FROM courses WHERE profesor_name = '{escaped_name}';")
            ref_count = db.execute(ref_query).scalar() or 0
            
            if ref_count > 0:
                print(f"  - {name} (referenced in {ref_count} courses)")
            else:
                print(f"  - {name}")

if __name__ == "__main__":
    asyncio.run(analyze_test_data())
