"""
Script to reset the database and import only data from orar.usv.ro
This script will:
1. Backup the current database (for safety)
2. Clear all existing data
3. Import fresh data from orar.usv.ro
4. Recreate essential system data (like admin users)
"""
import sys
import os
import datetime
from pathlib import Path
import asyncio
import aiohttp
import json
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import get_db
from app.core.config import settings
from app.core.security import get_password_hash

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

def backup_database():
    """
    Create a backup of the current database
    """
    try:
        print("Creating database backup...")
        
        # Get database connection details from settings
        db_user = settings.POSTGRES_USER
        db_password = settings.POSTGRES_PASSWORD
        db_name = settings.POSTGRES_DB
        db_host = settings.POSTGRES_SERVER
        
        # Create backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"db_backup_{timestamp}.sql"
        
        # Run pg_dump to create backup
        backup_command = f"pg_dump -h {db_host} -U {db_user} -d {db_name} -f {backup_file}"
        
        print(f"Running backup command: {backup_command}")
        print(f"Please enter the database password when prompted.")
        
        # Execute the backup command
        os.system(backup_command)
        
        print(f"Database backup created: {backup_file}")
        return True
        
    except Exception as e:
        print(f"Error creating database backup: {e}")
        return False

def reset_database():
    """
    Reset the database by dropping and recreating all tables
    """
    db = next(get_db())
    try:
        print("Resetting database...")
        
        # Drop all tables
        tables = [
            "exams",
            "courses",
            "professors",
            "sala",
            "grupa",
            "faculties",
            "users"
        ]
        
        for table in tables:
            try:
                drop_query = text(f"TRUNCATE TABLE {table} CASCADE;")
                db.execute(drop_query)
                print(f"Truncated table: {table}")
            except Exception as e:
                print(f"Error truncating table {table}: {e}")
        
        # Commit changes
        db.commit()
        print("Database reset successfully!")
        return True
        
    except Exception as e:
        print(f"Error resetting database: {e}")
        db.rollback()
        return False

def import_professors(professors_data):
    """
    Import professors from orar.usv.ro
    """
    db = next(get_db())
    try:
        print("Importing professors...")
        
        imported_count = 0
        
        for professor in professors_data:
            first_name = professor.get('firstName', '') or ''
            last_name = professor.get('lastName', '') or ''
            full_name = f"{first_name} {last_name}".strip()
            
            if not full_name or full_name == " ":
                continue
                
            email = professor.get('emailAddress', '') or ''
            phone = professor.get('phoneNumber', '') or ''
            faculty = professor.get('facultyName', '') or ''
            specialization = professor.get('departmentName', '') or ''
            
            # Insert professor
            insert_query = text("""
                INSERT INTO professors (name, email, phone, specialization, faculty, title)
                VALUES (:name, :email, :phone, :specialization, :faculty, :title)
                ON CONFLICT (name) DO UPDATE
                SET email = :email, phone = :phone, specialization = :specialization, faculty = :faculty
            """)
            
            db.execute(insert_query, {
                'name': full_name,
                'email': email,
                'phone': phone,
                'specialization': specialization,
                'faculty': faculty,
                'title': ''  # Default empty title
            })
            
            imported_count += 1
            
        # Commit changes
        db.commit()
        print(f"Imported {imported_count} professors")
        return imported_count
        
    except Exception as e:
        print(f"Error importing professors: {e}")
        db.rollback()
        return 0

def import_rooms(rooms_data):
    """
    Import rooms from orar.usv.ro
    """
    db = next(get_db())
    try:
        print("Importing rooms...")
        
        imported_count = 0
        
        for room in rooms_data:
            name = room.get('name', '') or ''
            
            if not name or name == " ":
                continue
                
            building = room.get('buildingName', '') or ''
            capacity = room.get('capacitate', '0') or '0'
            computers = room.get('computers', '0') or '0'
            
            # Convert to integers
            try:
                capacity = int(capacity)
            except:
                capacity = 0
                
            try:
                computers = int(computers)
            except:
                computers = 0
            
            # Insert room
            insert_query = text("""
                INSERT INTO sala (name, building, capacity, computers)
                VALUES (:name, :building, :capacity, :computers)
                ON CONFLICT (name) DO UPDATE
                SET building = :building, capacity = :capacity, computers = :computers
            """)
            
            db.execute(insert_query, {
                'name': name,
                'building': building,
                'capacity': capacity,
                'computers': computers
            })
            
            imported_count += 1
            
        # Commit changes
        db.commit()
        print(f"Imported {imported_count} rooms")
        return imported_count
        
    except Exception as e:
        print(f"Error importing rooms: {e}")
        db.rollback()
        return 0

def import_faculties(faculties_data):
    """
    Import faculties from orar.usv.ro
    """
    db = next(get_db())
    try:
        print("Importing faculties...")
        
        imported_count = 0
        
        for faculty in faculties_data:
            fid = faculty.get('id', '')
            
            if not fid:
                continue
                
            name = faculty.get('longName', '') or ''
            short_name = faculty.get('shortName', '') or ''
            
            # Insert faculty
            insert_query = text("""
                INSERT INTO faculties (id, name, short_name)
                VALUES (:id, :name, :short_name)
                ON CONFLICT (id) DO UPDATE
                SET name = :name, short_name = :short_name
            """)
            
            db.execute(insert_query, {
                'id': fid,
                'name': name,
                'short_name': short_name
            })
            
            imported_count += 1
            
        # Commit changes
        db.commit()
        print(f"Imported {imported_count} faculties")
        return imported_count
        
    except Exception as e:
        print(f"Error importing faculties: {e}")
        db.rollback()
        return 0

def import_groups(subgroups_data):
    """
    Import groups from orar.usv.ro
    """
    db = next(get_db())
    try:
        print("Importing groups...")
        
        imported_count = 0
        
        for subgroup in subgroups_data:
            name = subgroup.get('groupName', '') or ''
            
            if not name or name == " ":
                continue
                
            year = subgroup.get('studyYear', '0') or '0'
            specialization = subgroup.get('specializationShortName', '') or ''
            
            # Convert to integer
            try:
                year = int(year)
            except:
                year = 0
            
            # Insert group
            insert_query = text("""
                INSERT INTO grupa (name, year, specialization, leader_id)
                VALUES (:name, :year, :specialization, :leader_id)
                ON CONFLICT (name) DO UPDATE
                SET year = :year, specialization = :specialization
            """)
            
            db.execute(insert_query, {
                'name': name,
                'year': year,
                'specialization': specialization,
                'leader_id': None  # Default no leader
            })
            
            imported_count += 1
            
        # Commit changes
        db.commit()
        print(f"Imported {imported_count} groups")
        return imported_count
        
    except Exception as e:
        print(f"Error importing groups: {e}")
        db.rollback()
        return 0

def create_essential_users():
    """
    Create essential users for the system
    """
    db = next(get_db())
    try:
        print("Creating essential users...")
        
        # Create admin user
        admin_query = text("""
            INSERT INTO users (email, hashed_password, name, role)
            VALUES (:email, :hashed_password, :name, :role)
            ON CONFLICT (email) DO UPDATE
            SET hashed_password = :hashed_password, name = :name, role = :role
        """)
        
        db.execute(admin_query, {
            'email': 'admin@usv.ro',
            'hashed_password': get_password_hash('admin123'),
            'name': 'Admin USV',
            'role': 'ADMIN'
        })
        
        # Create secretariat user
        secretariat_query = text("""
            INSERT INTO users (email, hashed_password, name, role)
            VALUES (:email, :hashed_password, :name, :role)
            ON CONFLICT (email) DO UPDATE
            SET hashed_password = :hashed_password, name = :name, role = :role
        """)
        
        db.execute(secretariat_query, {
            'email': 'secretariat@usv.ro',
            'hashed_password': get_password_hash('secretariat123'),
            'name': 'Secretariat USV',
            'role': 'SECRETARIAT'
        })
        
        # Commit changes
        db.commit()
        print("Essential users created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating essential users: {e}")
        db.rollback()
        return False

async def main():
    print("=== DATABASE RESET AND IMPORT SCRIPT ===")
    print("This script will reset the database and import only data from orar.usv.ro")
    print("WARNING: All existing data will be lost!")
    print("Make sure you have a backup before proceeding.")
    
    print("\nDo you want to create a database backup before proceeding? (yes/no)")
    backup_answer = input().strip().lower()
    
    if backup_answer == 'yes':
        backup_success = backup_database()
        if not backup_success:
            print("Failed to create database backup. Aborting operation.")
            return
    
    print("\nDo you want to proceed with resetting the database? (yes/no)")
    reset_answer = input().strip().lower()
    
    if reset_answer != 'yes':
        print("Operation cancelled.")
        return
    
    # Reset database
    reset_success = reset_database()
    if not reset_success:
        print("Failed to reset database. Aborting operation.")
        return
    
    # Fetch data from orar.usv.ro
    print("\nFetching data from orar.usv.ro...")
    
    professors_data = await fetch_json_data(PROFESSORS_URL)
    rooms_data = await fetch_json_data(ROOMS_URL)
    faculties_data = await fetch_json_data(FACULTIES_URL)
    subgroups_data = await fetch_json_data(SUBGROUPS_URL)
    
    print(f"Fetched {len(professors_data)} professors")
    print(f"Fetched {len(rooms_data)} rooms")
    print(f"Fetched {len(faculties_data)} faculties")
    print(f"Fetched {len(subgroups_data)} subgroups")
    
    # Import data
    import_professors(professors_data)
    import_rooms(rooms_data)
    import_faculties(faculties_data)
    import_groups(subgroups_data)
    
    # Create essential users
    create_essential_users()
    
    print("\n=== DATABASE RESET AND IMPORT COMPLETED ===")
    print("The database now contains only data from orar.usv.ro and essential system data.")
    print("You can now start using the application with clean data.")

if __name__ == "__main__":
    asyncio.run(main())
