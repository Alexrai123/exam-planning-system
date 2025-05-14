import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.db.base import get_db, Base, engine
from app.models.user import User, UserRole
from app.models.grupa import Grupa
from app.core.security import get_password_hash

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

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
    db = next(get_db())
    
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
            
            # Check if group exists
            group = db.query(Grupa).filter(Grupa.name == group_name).first()
            if not group:
                errors.append(f"Group '{group_name}' not found")
                continue
                
            # Check if user already exists
            user = db.query(User).filter(User.email == email).first()
            
            if user:
                # Update existing user
                user.name = name
                user.role = UserRole.STUDENT
                print(f"Updated existing user: {name}")
            else:
                # Create new user
                user = User(
                    name=name,
                    email=email,
                    password=get_password_hash(default_password),
                    role=UserRole.STUDENT
                )
                db.add(user)
                db.flush()
                created_users += 1
                print(f"Created new user: {name}")
            
            # Update group with leader
            if group.leader_id != user.id:
                group.leader_id = user.id
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

if __name__ == "__main__":
    main()
