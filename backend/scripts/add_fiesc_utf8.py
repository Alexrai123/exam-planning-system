"""
Script to add FIESC specializations to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_fiesc_specializations():
    """
    Add FIESC specializations to the database
    """
    try:
        with engine.connect() as conn:
            # First check if FIESC faculty exists
            result = conn.execute(text(
                "SELECT id, name, short_name FROM faculties WHERE short_name = 'FIESC'"
            ))
            fiesc_faculty = result.fetchone()
            
            if fiesc_faculty:
                print(f"Found FIESC faculty with ID: {fiesc_faculty[0]}")
                fiesc_id = fiesc_faculty[0]
            else:
                # Get the next available faculty ID
                result = conn.execute(text("SELECT MAX(CAST(id AS INTEGER)) FROM faculties"))
                max_id = result.scalar() or 0
                next_id = str(int(max_id) + 1)
                
                print(f"FIESC faculty not found, creating it with ID: {next_id}")
                conn.execute(text(
                    "INSERT INTO faculties (id, name, short_name) VALUES (:id, :name, :short_name)"
                ), {
                    "id": next_id,
                    "name": "Facultatea de Inginerie Electrica si Stiinta Calculatoarelor",
                    "short_name": "FIESC"
                })
                conn.commit()
                
                fiesc_id = next_id
                print(f"Created FIESC faculty with ID: {fiesc_id}")
            
            # Define FIESC specializations
            fiesc_specializations = [
                {"name": "Calculatoare", "short_name": "CALC"},
                {"name": "Electronica aplicata", "short_name": "EA"},
                {"name": "Retele si software de telecomunicatii", "short_name": "RST"},
                {"name": "Sisteme electrice", "short_name": "SE"},
                {"name": "Energetica si tehnologii informatice", "short_name": "ETI"},
                {"name": "Managementul energiei", "short_name": "ME"},
                {"name": "Automatica si informatica aplicata", "short_name": "AIA"},
                {"name": "Echipamente si sisteme de comanda pentru autovehicule", "short_name": "ESCA"},
                {"name": "Echipamente si sisteme medicale", "short_name": "ESM"}
            ]
            
            # Add specializations
            specializations_added = 0
            print("\nAdding FIESC specializations to the database...")
            
            for spec in fiesc_specializations:
                # Check if specialization already exists
                result = conn.execute(text(
                    "SELECT id FROM specializations WHERE name = :name AND faculty_id = :faculty_id"
                ), {"name": spec["name"], "faculty_id": fiesc_id})
                
                if result.rowcount == 0:
                    # Add specialization
                    conn.execute(text(
                        "INSERT INTO specializations (name, short_name, faculty_id) VALUES (:name, :short_name, :faculty_id)"
                    ), {
                        "name": spec["name"],
                        "short_name": spec["short_name"],
                        "faculty_id": fiesc_id
                    })
                    
                    specializations_added += 1
                    print(f"Added: {spec['name']} ({spec['short_name']})")
                else:
                    print(f"Specialization already exists: {spec['name']}")
            
            conn.commit()
            print(f"Added {specializations_added} new FIESC specializations to the database")
            
            # List all faculties
            result = conn.execute(text(
                "SELECT id, name, short_name FROM faculties ORDER BY id"
            ))
            faculties = result.fetchall()
            
            print("\nAll faculties in database:")
            for faculty in faculties:
                print(f"ID: {faculty[0]}, Name: {faculty[1]}, Short Name: {faculty[2]}")
        
    except Exception as e:
        print(f"Error adding FIESC specializations: {e}")

if __name__ == "__main__":
    add_fiesc_specializations()
