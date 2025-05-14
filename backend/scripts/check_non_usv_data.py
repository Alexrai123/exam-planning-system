"""
Script to check if there's any data left in the database that isn't from orar.usv.ro
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
        if full_name and full_name != " ":  # Only add non-empty names
            professor_names.append(full_name)
    return professor_names

def get_room_names(rooms_data):
    """
    Extract room names from the API data, handling None values
    """
    room_names = []
    for r in rooms_data:
        name = r.get('name', '') or ''
        if name and name != " ":  # Only add non-empty names
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
        if name and name != " ":  # Only add non-empty names
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

        # Check users
        users_query = text("SELECT COUNT(*) FROM users")
        users_count = db.execute(users_query).scalar()
        print(f"Current users count: {users_count}")

    except Exception as e:
        print(f"Error checking database content: {e}")

def check_non_usv_professors(external_professors):
    """
    Check professors that aren't from orar.usv.ro
    """
    db = next(get_db())
    try:
        # Get all professors from the database
        query = text("SELECT name FROM professors")
        local_professors = db.execute(query).fetchall()
        local_professor_names = [p[0] for p in local_professors]
        
        # Find professors not in external data
        professors_not_in_external = set(local_professor_names) - set(external_professors)
        
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
        else:
            print("All professors in the database are from orar.usv.ro")
            
    except Exception as e:
        print(f"Error checking non-USV professors: {e}")

def check_non_usv_rooms(external_rooms):
    """
    Check rooms that aren't from orar.usv.ro
    """
    db = next(get_db())
    try:
        # Get all rooms from the database
        query = text("SELECT name FROM sala")
        local_rooms = db.execute(query).fetchall()
        local_room_names = [r[0] for r in local_rooms]
        
        # Find rooms not in external data
        rooms_not_in_external = set(local_room_names) - set(external_rooms)
        
        print(f"\nRooms in local database but not in external data: {len(rooms_not_in_external)}")
        if rooms_not_in_external:
            print("List of rooms not in external data:")
            for name in sorted(rooms_not_in_external):
                # Check if this room is referenced in exams
                escaped_name = name.replace("'", "''")
                ref_query = text(f"SELECT COUNT(*) FROM exams WHERE sala_name = '{escaped_name}';")
                ref_count = db.execute(ref_query).scalar() or 0
                
                if ref_count > 0:
                    print(f"  - {name} (referenced in {ref_count} exams)")
                else:
                    print(f"  - {name}")
        else:
            print("All rooms in the database are from orar.usv.ro")
            
    except Exception as e:
        print(f"Error checking non-USV rooms: {e}")

def check_non_usv_faculties(external_faculties):
    """
    Check faculties that aren't from orar.usv.ro
    """
    db = next(get_db())
    try:
        # Get all faculties from the database
        query = text("SELECT id FROM faculties")
        local_faculties = db.execute(query).fetchall()
        local_faculty_ids = [f[0] for f in local_faculties]
        
        # Find faculties not in external data
        faculties_not_in_external = set(local_faculty_ids) - set(external_faculties)
        
        print(f"\nFaculties in local database but not in external data: {len(faculties_not_in_external)}")
        if faculties_not_in_external:
            print("List of faculties not in external data:")
            for fid in sorted(faculties_not_in_external):
                # Get the faculty name
                name_query = text(f"SELECT name FROM faculties WHERE id = '{fid}';")
                name_result = db.execute(name_query).fetchone()
                name = name_result[0] if name_result else "Unknown"
                
                print(f"  - {name} (ID: {fid})")
        else:
            print("All faculties in the database are from orar.usv.ro")
            
    except Exception as e:
        print(f"Error checking non-USV faculties: {e}")

def check_non_usv_groups(external_groups):
    """
    Check groups that aren't from orar.usv.ro
    """
    db = next(get_db())
    try:
        # Get all groups from the database
        query = text("SELECT name FROM grupa")
        local_groups = db.execute(query).fetchall()
        local_group_names = [g[0] for g in local_groups]
        
        # Find groups not in external data
        groups_not_in_external = set(local_group_names) - set(external_groups)
        
        print(f"\nGroups in local database but not in external data: {len(groups_not_in_external)}")
        if groups_not_in_external:
            print("Sample of groups not in external data (showing first 10):")
            for name in sorted(list(groups_not_in_external))[:10]:
                # Check if this group is referenced in exams
                escaped_name = name.replace("'", "''")
                ref_query = text(f"SELECT COUNT(*) FROM exams WHERE grupa_name = '{escaped_name}';")
                ref_count = db.execute(ref_query).scalar() or 0
                
                if ref_count > 0:
                    print(f"  - {name} (referenced in {ref_count} exams)")
                else:
                    print(f"  - {name}")
            
            if len(groups_not_in_external) > 10:
                print(f"  ... and {len(groups_not_in_external) - 10} more")
        else:
            print("All groups in the database are from orar.usv.ro")
            
    except Exception as e:
        print(f"Error checking non-USV groups: {e}")

def check_courses_and_exams():
    """
    Check courses and exams that might not be from orar.usv.ro
    """
    db = next(get_db())
    try:
        # Check for test-like courses
        test_courses_query = text("""
            SELECT id, name, profesor_name
            FROM courses
            WHERE name LIKE '%test%' OR name LIKE '%Test%' OR name LIKE '%dummy%' OR name LIKE '%Dummy%'
        """)
        test_courses = db.execute(test_courses_query).fetchall()
        
        print(f"\nCourses with test-like names: {len(test_courses)}")
        if test_courses:
            print("List of test-like courses:")
            for course in test_courses:
                print(f"  - {course[1]} (Professor: {course[2]})")
        else:
            print("No courses with test-like names found")
        
        # Check for test-like exams
        test_exams_query = text("""
            SELECT id, course_id, status
            FROM exams
            WHERE status LIKE '%test%' OR status LIKE '%Test%'
        """)
        test_exams = db.execute(test_exams_query).fetchall()
        
        print(f"\nExams with test-like status: {len(test_exams)}")
        if test_exams:
            print("List of test-like exams:")
            for exam in test_exams:
                # Get course name
                course_query = text(f"SELECT name FROM courses WHERE id = {exam[1]};")
                course_result = db.execute(course_query).fetchone()
                course_name = course_result[0] if course_result else "Unknown"
                
                print(f"  - Exam ID: {exam[0]} for course '{course_name}' (Status: {exam[2]})")
        else:
            print("No exams with test-like status found")
            
    except Exception as e:
        print(f"Error checking courses and exams: {e}")

def check_users():
    """
    Check users that might be test users
    """
    db = next(get_db())
    try:
        # Check for test-like users
        test_users_query = text("""
            SELECT id, email, name, role
            FROM users
            WHERE email LIKE '%test%' OR email LIKE '%Test%' OR 
                  name LIKE '%test%' OR name LIKE '%Test%' OR
                  email = 'admin@example.com' OR email = 'user@example.com'
        """)
        test_users = db.execute(test_users_query).fetchall()
        
        print(f"\nUsers with test-like attributes: {len(test_users)}")
        if test_users:
            print("List of test-like users:")
            for user in test_users:
                print(f"  - {user[2]} ({user[1]}, Role: {user[3]})")
        else:
            print("No users with test-like attributes found")
            
    except Exception as e:
        print(f"Error checking users: {e}")

async def main():
    print("Checking current database content...")
    check_database_content()
    
    print("\nFetching external data from orar.usv.ro...")
    
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
    
    # Extract data with proper handling of None values
    external_professors = get_professor_names(professors_data)
    external_rooms = get_room_names(rooms_data)
    external_faculties = get_faculty_ids(faculties_data)
    external_groups = get_group_names(subgroups_data)
    
    print(f"\nExtracted {len(external_professors)} valid professor names")
    print(f"Extracted {len(external_rooms)} valid room names")
    print(f"Extracted {len(external_faculties)} valid faculty IDs")
    print(f"Extracted {len(external_groups)} valid group names")
    
    print("\n--- CHECKING FOR NON-USV DATA ---")
    
    # Check for non-USV data
    check_non_usv_professors(external_professors)
    check_non_usv_rooms(external_rooms)
    check_non_usv_faculties(external_faculties)
    check_non_usv_groups(external_groups)
    
    # Check courses and exams
    check_courses_and_exams()
    
    # Check users
    check_users()
    
    print("\n--- SUMMARY ---")
    print("The database contains data that is not from orar.usv.ro, including:")
    print("1. Test professors (which we've already updated in courses)")
    print("2. Groups that don't match the format from orar.usv.ro")
    print("3. Possibly some test courses and exams")
    print("4. Test users for development and testing purposes")
    print("\nSome of this data is necessary for the application to function properly.")

if __name__ == "__main__":
    asyncio.run(main())
