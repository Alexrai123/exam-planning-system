"""
Script to create essential users for the system
"""
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import get_db
from app.core.security import get_password_hash

def create_essential_users():
    """
    Create essential users for the system
    """
    db = next(get_db())
    try:
        print("Creating essential users...")
        
        # Create admin user (using SECRETARIAT role since there's no ADMIN role)
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
            'role': 'SECRETARIAT'
        })
        
        # Create secretariat user
        secretariat_query = text("""
            INSERT INTO users (email, password, name, role)
            VALUES (:email, :password, :name, :role)
            ON CONFLICT (email) DO UPDATE
            SET password = :password, name = :name, role = :role
        """)
        
        db.execute(secretariat_query, {
            'email': 'secretariat@usv.ro',
            'password': get_password_hash('secretariat123'),
            'name': 'Secretariat USV',
            'role': 'SECRETARIAT'
        })
        
        # Create professor user
        professor_query = text("""
            INSERT INTO users (email, password, name, role)
            VALUES (:email, :password, :name, :role)
            ON CONFLICT (email) DO UPDATE
            SET password = :password, name = :name, role = :role
        """)
        
        db.execute(professor_query, {
            'email': 'professor@usv.ro',
            'password': get_password_hash('professor123'),
            'name': 'Professor USV',
            'role': 'PROFESSOR'
        })
        
        # Create student user
        student_query = text("""
            INSERT INTO users (email, password, name, role)
            VALUES (:email, :password, :name, :role)
            ON CONFLICT (email) DO UPDATE
            SET password = :password, name = :name, role = :role
        """)
        
        db.execute(student_query, {
            'email': 'student@usv.ro',
            'password': get_password_hash('student123'),
            'name': 'Student USV',
            'role': 'STUDENT'
        })
        
        # Commit changes
        db.commit()
        print("Essential users created successfully!")
        
        # Print login credentials
        print("\nLogin Credentials:")
        print("------------------")
        print("Admin User:")
        print("  Email: admin@usv.ro")
        print("  Password: admin123")
        print("  Role: SECRETARIAT (Admin)")
        print("\nSecretariat User:")
        print("  Email: secretariat@usv.ro")
        print("  Password: secretariat123")
        print("  Role: SECRETARIAT")
        print("\nProfessor User:")
        print("  Email: professor@usv.ro")
        print("  Password: professor123")
        print("  Role: PROFESSOR")
        print("\nStudent User:")
        print("  Email: student@usv.ro")
        print("  Password: student123")
        print("  Role: STUDENT")
        
        return True
        
    except Exception as e:
        print(f"Error creating essential users: {e}")
        db.rollback()
        return False

if __name__ == "__main__":
    create_essential_users()
