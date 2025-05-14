import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create a direct database connection
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/exam_planning"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Group data
groups = [
    {"name": "CALC1A", "year": 1, "specialization": "Computer Science"},
    {"name": "3111", "year": 3, "specialization": "Computer Science"},
    {"name": "3211", "year": 3, "specialization": "Information Technology"},
    {"name": "3212", "year": 3, "specialization": "Information Technology"},
    {"name": "3221", "year": 3, "specialization": "Cybersecurity"},
    {"name": "3231", "year": 3, "specialization": "Artificial Intelligence"},
    {"name": "3241", "year": 3, "specialization": "Data Science"},
    {"name": "3112", "year": 3, "specialization": "Computer Science"},
    {"name": "3113", "year": 3, "specialization": "Computer Science"},
    {"name": "3114", "year": 3, "specialization": "Computer Science"},
    {"name": "3121", "year": 3, "specialization": "Computer Engineering"}
]

def main():
    # Get DB session
    db = SessionLocal()
    
    created_groups = 0
    updated_groups = 0
    errors = []
    
    for group_data in groups:
        try:
            name = group_data["name"]
            year = group_data["year"]
            specialization = group_data["specialization"]
            
            # Check if group already exists
            group_result = db.execute(
                text("SELECT name FROM grupa WHERE name = :name"),
                {"name": name}
            ).fetchone()
            
            if group_result:
                # Update existing group
                db.execute(
                    text("UPDATE grupa SET year = :year, specialization = :specialization WHERE name = :name"),
                    {"year": year, "specialization": specialization, "name": name}
                )
                updated_groups += 1
                print(f"Updated existing group: {name}")
            else:
                # Create new group
                db.execute(
                    text("INSERT INTO grupa (name, year, specialization) VALUES (:name, :year, :specialization)"),
                    {"name": name, "year": year, "specialization": specialization}
                )
                created_groups += 1
                print(f"Created new group: {name}")
            
            # Commit changes for this group
            db.commit()
            
        except Exception as e:
            db.rollback()
            errors.append(f"Error processing {group_data['name']}: {str(e)}")
            print(f"Error: {str(e)}")
    
    print(f"\nSummary:")
    print(f"Created groups: {created_groups}")
    print(f"Updated groups: {updated_groups}")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
    
    db.close()

if __name__ == "__main__":
    main()
