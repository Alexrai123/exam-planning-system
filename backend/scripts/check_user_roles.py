"""
Script to check the valid user roles in the database
"""
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db

def check_user_roles():
    """Check the valid user roles in the database"""
    db = next(get_db())
    try:
        # Check the enum type for user roles
        enum_query = text("""
            SELECT e.enumlabel
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid 
            JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            WHERE t.typname = 'userrole'
        """)
        enum_values = db.execute(enum_query).fetchall()
        
        print("\nValid user roles:")
        for value in enum_values:
            print(f"  {value[0]}")
        
    except Exception as e:
        print(f"Error checking user roles: {e}")

if __name__ == "__main__":
    check_user_roles()
