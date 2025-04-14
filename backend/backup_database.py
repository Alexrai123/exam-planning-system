import os
import datetime
import subprocess
from app.core.config import settings

def backup_database():
    """
    Create a backup of the PostgreSQL database
    """
    # Get database connection details from settings
    db_url = settings.DATABASE_URL
    # Parse the database URL to get components
    db_parts = db_url.replace("postgresql://", "").split("/")
    db_auth = db_parts[0].split("@")
    
    db_user_pass = db_auth[0].split(":")
    db_user = db_user_pass[0]
    db_pass = db_user_pass[1] if len(db_user_pass) > 1 else ""
    
    db_host_port = db_auth[1].split(":")
    db_host = db_host_port[0]
    db_port = db_host_port[1] if len(db_host_port) > 1 else "5432"
    
    db_name = db_parts[1]
    
    # Create backup directory if it doesn't exist
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")
    
    # Set environment variables for pg_dump
    env = os.environ.copy()
    env["PGPASSWORD"] = db_pass
    
    # Construct the pg_dump command
    command = [
        "pg_dump",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-F", "c",  # Custom format (compressed)
        "-b",  # Include large objects
        "-v",  # Verbose
        "-f", backup_file,
        db_name
    ]
    
    try:
        # Execute the backup command
        result = subprocess.run(command, env=env, check=True, capture_output=True)
        print(f"Database backup created successfully: {backup_file}")
        print(result.stdout.decode())
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Error creating database backup: {e}")
        print(e.stderr.decode())
        return None

if __name__ == "__main__":
    backup_database()
