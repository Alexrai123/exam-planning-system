import asyncio
import aiohttp
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("POSTGRES_HOST", "exam_planning_db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "exam_planning")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# URLs for external data
PROFESSORS_URL = "https://orar.usv.ro/orar/vizualizare/data/cadre.php?json"
ROOMS_URL = "https://orar.usv.ro/orar/vizualizare/data/sali.php?json"
FACULTIES_URL = "https://orar.usv.ro/orar/vizualizare/data/facultati.php?json"
SUBGROUPS_URL = "https://orar.usv.ro/orar/vizualizare/data/subgrupe.php?json"

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = True
    return conn

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

async def import_faculties():
    """
    Import faculties directly into the database
    """
    print("Importing faculties...")
    faculties_data = await fetch_json_data(FACULTIES_URL)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create faculties table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculties (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            short_name VARCHAR(20)
        )
    """)
    
    # Map of faculty short names to full names (since the API doesn't provide full names)
    faculty_names = {
        "FIESC": "Facultatea de Inginerie Electrică și Știința Calculatoarelor",
        "FIMAR": "Facultatea de Inginerie Mecanică, Autovehicule și Robotică",
        "FEFS": "Facultatea de Educație Fizică și Sport",
        "FIA": "Facultatea de Inginerie Alimentară",
        "FIG": "Facultatea de Istorie și Geografie",
        "FLSC": "Facultatea de Litere și Științe ale Comunicării",
        "FS": "Facultatea de Silvicultură",
        "FEAA": "Facultatea de Economie, Administrație și Afaceri",
        "FSE": "Facultatea de Științe ale Educației",
        "FDSA": "Facultatea de Drept și Științe Administrative",
        "DSPP": "Departamentul de Specialitate cu Profil Psihopedagogic",
        "FMSB": "Facultatea de Medicină și Științe Biologice",
        "CSUD": "Consiliul Studiilor Universitare de Doctorat"
    }
    
    imported_count = 0
    updated_count = 0
    
    for faculty in faculties_data:
        faculty_id = faculty.get('id', '')
        short_name = faculty.get('shortName', '')
        
        # Skip if no id or short_name
        if not faculty_id or not short_name:
            continue
            
        # Get full name from our mapping
        name = faculty_names.get(short_name, f"Faculty {short_name}")
            
        # Check if faculty already exists
        cursor.execute("SELECT id FROM faculties WHERE id = %s", (faculty_id,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing faculty
            cursor.execute("""
                UPDATE faculties 
                SET name = %s, short_name = %s
                WHERE id = %s
            """, (name, short_name, faculty_id))
            updated_count += 1
        else:
            # Create new faculty
            cursor.execute("""
                INSERT INTO faculties (id, name, short_name)
                VALUES (%s, %s, %s)
            """, (faculty_id, name, short_name))
            imported_count += 1
    
    conn.close()
    print(f"Faculties imported: {imported_count} new, {updated_count} updated")
    return imported_count, updated_count

async def import_professors():
    """
    Import professors directly into the database
    """
    print("Importing professors...")
    professors_data = await fetch_json_data(PROFESSORS_URL)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported_count = 0
    updated_count = 0
    
    for professor in professors_data:
        # Combine first and last name
        full_name = f"{professor.get('firstName', '')} {professor.get('lastName', '')}".strip()
        
        # Skip if no name
        if not full_name:
            continue
            
        # Check if professor already exists
        cursor.execute("SELECT name FROM professors WHERE name = %s", (full_name,))
        existing = cursor.fetchone()
        
        specialization = professor.get('departmentName', '')
        email = professor.get('emailAddress', '')
        phone = professor.get('phoneNumber', '')
        faculty = professor.get('facultyName', '')
        
        if existing:
            # Update existing professor
            cursor.execute("""
                UPDATE professors 
                SET specialization = %s, email = %s, phone = %s, faculty = %s
                WHERE name = %s
            """, (specialization, email, phone, faculty, full_name))
            updated_count += 1
        else:
            # Create new professor
            cursor.execute("""
                INSERT INTO professors (name, specialization, title, email, phone, faculty)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (full_name, specialization, "", email, phone, faculty))
            imported_count += 1
    
    conn.close()
    print(f"Professors imported: {imported_count} new, {updated_count} updated")
    return imported_count, updated_count

async def import_rooms():
    """
    Import rooms directly into the database
    """
    print("Importing rooms...")
    rooms_data = await fetch_json_data(ROOMS_URL)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported_count = 0
    updated_count = 0
    
    for room in rooms_data:
        room_name = room.get('name', '')
        
        # Skip if no name
        if not room_name:
            continue
            
        # Check if room already exists
        cursor.execute("SELECT name FROM sala WHERE name = %s", (room_name,))
        existing = cursor.fetchone()
        
        building = room.get('buildingName', '')
        capacity = int(room.get('capacitate', 0)) if room.get('capacitate', '').isdigit() else 0
        computers = int(room.get('computers', 0)) if room.get('computers', '').isdigit() else 0
        
        if existing:
            # Update existing room
            cursor.execute("""
                UPDATE sala 
                SET building = %s, capacity = %s, computers = %s
                WHERE name = %s
            """, (building, capacity, computers, room_name))
            updated_count += 1
        else:
            # Create new room
            cursor.execute("""
                INSERT INTO sala (name, building, capacity, computers)
                VALUES (%s, %s, %s, %s)
            """, (room_name, building, capacity, computers))
            imported_count += 1
    
    conn.close()
    print(f"Rooms imported: {imported_count} new, {updated_count} updated")
    return imported_count, updated_count

async def import_groups():
    """
    Import groups directly into the database
    """
    print("Importing groups...")
    subgroups_data = await fetch_json_data(SUBGROUPS_URL)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported_count = 0
    updated_count = 0
    
    for subgroup in subgroups_data:
        # Create a name that combines year, group name and subgroup index
        name = f"{subgroup.get('studyYear', '')}{subgroup.get('groupName', '')}{subgroup.get('subgroupIndex', '')}"
        
        # Skip if no name
        if not name:
            continue
            
        # Check if group already exists
        cursor.execute("SELECT name FROM grupa WHERE name = %s", (name,))
        existing = cursor.fetchone()
        
        year = int(subgroup.get('studyYear', 0)) if subgroup.get('studyYear', '').isdigit() else 0
        specialization = subgroup.get('specializationShortName', '')
        
        if existing:
            # Update existing group
            cursor.execute("""
                UPDATE grupa 
                SET year = %s, specialization = %s
                WHERE name = %s
            """, (year, specialization, name))
            updated_count += 1
        else:
            # Create new group
            cursor.execute("""
                INSERT INTO grupa (name, year, specialization)
                VALUES (%s, %s, %s)
            """, (name, year, specialization))
            imported_count += 1
    
    conn.close()
    print(f"Groups imported: {imported_count} new, {updated_count} updated")
    return imported_count, updated_count

async def main():
    """
    Main function to import all data
    """
    print("Starting direct data import...")
    
    # Import faculties
    faculties_imported, faculties_updated = await import_faculties()
    
    # Import professors
    professors_imported, professors_updated = await import_professors()
    
    # Import rooms
    rooms_imported, rooms_updated = await import_rooms()
    
    # Import groups
    groups_imported, groups_updated = await import_groups()
    
    print("\nImport completed!")
    print(f"Faculties: {faculties_imported} new, {faculties_updated} updated")
    print(f"Professors: {professors_imported} new, {professors_updated} updated")
    print(f"Rooms: {rooms_imported} new, {rooms_updated} updated")
    print(f"Groups: {groups_imported} new, {groups_updated} updated")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
