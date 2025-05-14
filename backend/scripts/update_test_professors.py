"""
Script to safely update test professors to reference real professors from orar.usv.ro
"""
import sys
import os
from pathlib import Path
import asyncio
import aiohttp
import json
import random

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db

# URLs for external data
PROFESSORS_URL = "https://orar.usv.ro/orar/vizualizare/data/cadre.php?json"

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

def identify_test_professors():
    """
    Identify test professors in the database
    """
    db = next(get_db())
    try:
        # Get professors with test-like names
        test_query = text("""
            SELECT name
            FROM professors
            WHERE name LIKE '%test%' OR name LIKE '%Test%' OR name = 'John Smith' OR name = 'None None'
        """)
        test_professors = db.execute(test_query).fetchall()
        
        return [prof[0] for prof in test_professors]
        
    except Exception as e:
        print(f"Error identifying test professors: {e}")
        return []

def get_courses_with_test_professors(test_professors):
    """
    Get courses that reference test professors
    """
    db = next(get_db())
    courses_with_test_professors = []
    
    try:
        for professor in test_professors:
            escaped_name = professor.replace("'", "''")
            query = text(f"""
                SELECT id, name, profesor_name
                FROM courses
                WHERE profesor_name = '{escaped_name}'
            """)
            courses = db.execute(query).fetchall()
            
            for course in courses:
                courses_with_test_professors.append({
                    'id': course[0],
                    'name': course[1],
                    'professor': course[2]
                })
                
        return courses_with_test_professors
        
    except Exception as e:
        print(f"Error getting courses with test professors: {e}")
        return []

def update_courses_with_real_professors(courses, real_professors):
    """
    Update courses to reference real professors
    """
    if not real_professors:
        print("No real professors available for update")
        return False
        
    db = next(get_db())
    try:
        print("\nUpdating courses to reference real professors...")
        
        for course in courses:
            # Select a random real professor
            new_professor = random.choice(real_professors)
            
            # Update the course
            escaped_old_name = course['professor'].replace("'", "''")
            escaped_new_name = new_professor.replace("'", "''")
            
            update_query = text(f"""
                UPDATE courses
                SET profesor_name = '{escaped_new_name}'
                WHERE id = {course['id']} AND profesor_name = '{escaped_old_name}'
            """)
            
            result = db.execute(update_query)
            
            if result.rowcount > 0:
                print(f"Updated course '{course['name']}' from '{course['professor']}' to '{new_professor}'")
            else:
                print(f"Failed to update course '{course['name']}'")
        
        # Commit changes
        db.commit()
        print("Courses updated successfully!")
        return True
        
    except Exception as e:
        print(f"Error updating courses: {e}")
        db.rollback()
        return False

def delete_test_professors(test_professors):
    """
    Delete test professors from the database
    """
    db = next(get_db())
    try:
        print("\nDeleting test professors...")
        
        for professor in test_professors:
            escaped_name = professor.replace("'", "''")
            delete_query = text(f"""
                DELETE FROM professors
                WHERE name = '{escaped_name}'
            """)
            
            result = db.execute(delete_query)
            
            if result.rowcount > 0:
                print(f"Deleted test professor: {professor}")
            else:
                print(f"Failed to delete professor: {professor}")
        
        # Commit changes
        db.commit()
        print("Test professors deleted successfully!")
        
    except Exception as e:
        print(f"Error deleting test professors: {e}")
        db.rollback()

async def main():
    print("Fetching real professors from orar.usv.ro...")
    
    # Fetch professors data
    professors_data = await fetch_json_data(PROFESSORS_URL)
    
    # Extract professor names
    real_professors = get_professor_names(professors_data)
    print(f"Fetched {len(real_professors)} real professors")
    
    # Identify test professors
    test_professors = identify_test_professors()
    print(f"\nIdentified {len(test_professors)} test professors:")
    for prof in test_professors:
        print(f"  - {prof}")
    
    # Get courses with test professors
    courses = get_courses_with_test_professors(test_professors)
    print(f"\nFound {len(courses)} courses referencing test professors:")
    for course in courses:
        print(f"  - {course['name']} (Professor: {course['professor']})")
    
    # Automatically proceed with updates
    print("\nAutomatically updating courses to reference real professors...")
    
    # Update courses with real professors
    success = update_courses_with_real_professors(courses, real_professors)
    
    if success:
        # Don't automatically delete professors to be safe
        print("\nCourses updated successfully.")
        print("Test professors were not deleted to maintain database integrity.")
        print("You can manually delete them later if needed.")
    else:
        print("Failed to update courses. Test professors not deleted.")


if __name__ == "__main__":
    asyncio.run(main())
