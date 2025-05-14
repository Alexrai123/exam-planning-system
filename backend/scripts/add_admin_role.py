"""
Script to add the ADMIN role to the userrole enum in the database
"""
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db
from app.core.security import get_password_hash

def add_admin_role():
    """Add the ADMIN role to the userrole enum in the database"""
    db = next(get_db())
    try:
        print("Adding ADMIN role to the userrole enum...")
        
        # Check if ADMIN role already exists
        check_query = text("""
            SELECT e.enumlabel
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid 
            JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            WHERE t.typname = 'userrole' AND e.enumlabel = 'ADMIN'
        """)
        
        result = db.execute(check_query).fetchone()
        
        if result:
            print("ADMIN role already exists in the userrole enum")
        else:
            # Add ADMIN role to the userrole enum
            add_query = text("""
                ALTER TYPE userrole ADD VALUE 'ADMIN'
            """)
            
            db.execute(add_query)
            db.commit()
            print("ADMIN role added to the userrole enum")
        
        # Create admin user
        admin_query = text("""
            INSERT INTO users (email, password, name, role)
            VALUES (:email, :password, :name, :role)
            ON CONFLICT (email) DO UPDATE
            SET password = :password, name = :name, role = :role
        """)
        
        db.execute(admin_query, {
            'email': 'admin@usv.ro',
            'password': get_password_hash('admin123'),
            'name': 'Admin USV',
            'role': 'ADMIN'
        })
        
        db.commit()
        print("Admin user created/updated successfully")
        
        # Print login credentials
        print("\nAdmin User Login Credentials:")
        print("Email: admin@usv.ro")
        print("Password: admin123")
        print("Role: ADMIN")
        
    except Exception as e:
        print(f"Error adding ADMIN role: {e}")
        db.rollback()

if __name__ == "__main__":
    add_admin_role()
