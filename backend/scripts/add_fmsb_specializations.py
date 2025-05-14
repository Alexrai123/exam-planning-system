"""
Script to add FMSB specializations to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine, get_db
from app.models.faculty import Faculty

def add_fmsb_specializations():
    """
    Add FMSB specializations to the database
    """
    try:
        db = next(get_db())
        
        # Check if FMSB faculty exists
        fmsb = db.query(Faculty).filter(Faculty.id == "21").first()
        if not fmsb:
            print("FMSB faculty not found in the database.")
            return
        
        print(f"Faculty ID: 21 (FMSB) exists in the database.")
        
        # Define FMSB specializations
        specializations = [
            "Medicina",
            "Asistenta medicala generala",
            "Balneofiziokinetoterapie si recuperare",
            "Biochimie",
            "Biologie",
            "Nutritie si dietetica",
            "Tehnica dentara",
            "Master - Nutritie si Recuperare Medicala"
        ]
        
        # Check if specializations table exists
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_name = 'specializations'"
            ))
            if result.rowcount == 0:
                # Create specializations table if it doesn't exist
                print("Creating specializations table...")
                conn.execute(text("""
                    CREATE TABLE specializations (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        faculty_id VARCHAR(10) REFERENCES faculties(id),
                        short_name VARCHAR(20),
                        description TEXT
                    )
                """))
                conn.commit()
                print("Specializations table created.")
            
            # Add specializations to the database
            print("\nAdding FMSB specializations:")
            print("-" * 80)
            
            for spec in specializations:
                # Check if specialization already exists
                result = conn.execute(text(
                    "SELECT id FROM specializations WHERE name = :name AND faculty_id = :faculty_id"
                ), {"name": spec, "faculty_id": "21"})
                
                if result.rowcount > 0:
                    print(f"Specialization '{spec}' already exists")
                else:
                    # Generate short name from first letters of words
                    words = spec.split()
                    short_name = ''.join([word[0] for word in words if word not in ['si', '-']])
                    
                    # Insert specialization
                    conn.execute(text(
                        "INSERT INTO specializations (name, faculty_id, short_name) VALUES (:name, :faculty_id, :short_name)"
                    ), {"name": spec, "faculty_id": "21", "short_name": short_name})
                    
                    print(f"Added: {spec}")
            
            conn.commit()
            print("-" * 80)
            
            # List all specializations
            result = conn.execute(text(
                "SELECT id, name, faculty_id, short_name FROM specializations WHERE faculty_id = '21'"
            ))
            rows = result.fetchall()
            
            print(f"\nFMSB Specializations in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Short Name':<15}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<50} {row[3]:<15}")
            
            print("-" * 80)
            print("\nSpecializations added successfully. You can now add courses for each specialization.")
        
    except Exception as e:
        print(f"Error adding FMSB specializations: {e}")

if __name__ == "__main__":
    add_fmsb_specializations()
