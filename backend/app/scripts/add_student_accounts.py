import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
from app.core.config import settings

# Create a direct database connection
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/exam_planning"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Group leaders data
group_leaders = [
    {"name": "John Doe", "email": "john.doe@student.usv.ro", "group": "CALC1A"},
    {"name": "Jane Smith", "email": "jane.smith@student.usv.ro", "group": "3111"},
    {"name": "Maria Popescu", "email": "maria.popescu@student.usv.ro", "group": "3211"},
    {"name": "Alexandru Ionescu", "email": "alexandru.ionescu@student.usv.ro", "group": "3212"},
    {"name": "Elena Dumitrescu", "email": "elena.dumitrescu@student.usv.ro", "group": "3221"},
    {"name": "Andrei Constantinescu", "email": "andrei.constantinescu@student.usv.ro", "group": "3231"},
    {"name": "Cristina Georgescu", "email": "cristina.georgescu@student.usv.ro", "group": "3241"},
    {"name": "Mihai Stanescu", "email": "mihai.stanescu@student.usv.ro", "group": "3112"},
    {"name": "Laura Vasilescu", "email": "laura.vasilescu@student.usv.ro", "group": "3113"},
    {"name": "Bogdan Marinescu", "email": "bogdan.marinescu@student.usv.ro", "group": "3114"},
    {"name": "Ana Petrescu", "email": "ana.petrescu@student.usv.ro", "group": "3121"}
]

def main():
    # Get DB session
    db = SessionLocal()
    
    created_users = 0
    updated_groups = 0
    errors = []
    
    # Default password for all users
    default_password = "student123"
    
    for leader in group_leaders:
        try:
            name = leader["name"]
            email = leader["email"]
            group_name = leader["group"]
            
            # Check if group exists using raw SQL
            group_result = db.execute(text(f"SELECT name FROM grupa WHERE name = :name"), {"name": group_name}).fetchone()
            if not group_result:
                errors.append(f"Group '{group_name}' not found")
                continue
                
            group_name = group_result[0]
                
            # Check if user already exists
            user_result = db.execute(text("SELECT id, role FROM users WHERE email = :email"), {"email": email}).fetchone()
            
            if user_result:
                # Update existing user
                user_id = user_result[0]
                db.execute(
                    text("UPDATE users SET name = :name, role = 'STUDENT' WHERE id = :id"),
                    {"name": name, "id": user_id}
                )
                print(f"Updated existing user: {name}")
            else:
                # Create new user with raw SQL
                hashed_password = get_password_hash(default_password)
                result = db.execute(
                    text("INSERT INTO users (name, email, password, role) VALUES (:name, :email, :password, 'STUDENT') RETURNING id"),
                    {"name": name, "email": email, "password": hashed_password}
                )
                user_id = result.fetchone()[0]
                created_users += 1
                print(f"Created new user: {name}")
            
            # Update group with leader
            group_leader_result = db.execute(
                text("SELECT leader_id FROM grupa WHERE name = :name"),
                {"name": group_name}
            ).fetchone()
            
            if not group_leader_result[0] or group_leader_result[0] != user_id:
                db.execute(
                    text("UPDATE grupa SET leader_id = :leader_id WHERE name = :name"),
                    {"leader_id": user_id, "name": group_name}
                )
                updated_groups += 1
                print(f"Set {name} as leader for group {group_name}")
            
            # Commit changes for this user
            db.commit()
            
        except Exception as e:
            db.rollback()
            errors.append(f"Error processing {leader['name']}: {str(e)}")
            print(f"Error: {str(e)}")
    
    print(f"\nSummary:")
    print(f"Created users: {created_users}")
    print(f"Updated groups: {updated_groups}")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
    
    db.close()

if __name__ == "__main__":
    main()
