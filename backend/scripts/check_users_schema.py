"""
Script to check the users table schema
"""
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db

def check_users_schema():
    """Check the users table schema"""
    db = next(get_db())
    try:
        # Check users table schema
        users_schema = text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
        """)
        users_columns = db.execute(users_schema).fetchall()
        print("\nUsers table schema:")
        for column in users_columns:
            print(f"  {column[0]} ({column[1]})")
        
    except Exception as e:
        print(f"Error checking users schema: {e}")

if __name__ == "__main__":
    check_users_schema()
