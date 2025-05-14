"""
Script to add FIESC (Facultatea de Inginerie Electrica si Stiinta Calculatoarelor) specializations to the database
Using ASCII characters only to avoid encoding issues
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_fiesc_faculty_and_specializations():
    """
    Add FIESC faculty and specializations to the database
    """
    try:
        with engine.connect() as conn:
            # First check if FIESC faculty exists
            result = conn.execute(text(
                "SELECT id, name, short_name FROM faculties WHERE short_name = 'FIESC'"
            ))
            fiesc_faculty = result.fetchone()
            
            if fiesc_faculty:
                print(f"Found FIESC faculty with ID: {fiesc_faculty[0]}, Name: {fiesc_faculty[1]}, Short Name: {fiesc_faculty[2]}")
                fiesc_id = fiesc_faculty[0]
            else:
                # Get the next available faculty ID
                result = conn.execute(text("SELECT MAX(CAST(id AS INTEGER)) FROM faculties"))
                max_id = result.scalar() or 0
                next_id = str(int(max_id) + 1)
                
                print(f"FIESC faculty not found, creating it with ID: {next_id}...")
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
            
            # Define FIESC specializations from the provided image (ASCII only)
            fiesc_specializations = [
                {"name": "Calculatoare", "short_name": "CALC"},
                {"name": "Electronica aplicata", "short_name": "EA"},
                {"name": "Retele si software de telecomunicatii", "short_name": "RST"},
                {"name": "Sisteme electrice", "short_name": "SE"},
                {"name": "Energetica si tehnologii informatice", "short_name": "ETI"},
                {"name": "Managementul energiei", "short_name": "ME"},
                {"name": "Automatica si informatica aplicata", "short_name": "AIA"},
                {"name": "Echipamente si sisteme de comanda si control pentru autovehicule", "short_name": "ESCCA"},
                {"name": "Echipamente si sisteme medicale", "short_name": "ESM"}
            ]
            
            # Add specializations
            specializations_added = 0
            print("\nAdding FIESC specializations to the database...")
            print("-" * 80)
            
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
            print("-" * 80)
            print(f"Added {specializations_added} new FIESC specializations to the database")
            
            # List all FIESC specializations
            result = conn.execute(text(
                """
                SELECT s.id, s.name, s.short_name, f.name as faculty_name
                FROM specializations s
                JOIN faculties f ON s.faculty_id = f.id
                WHERE s.faculty_id = :faculty_id
                ORDER BY s.name
                """
            ), {"faculty_id": fiesc_id})
            rows = result.fetchall()
            
            print(f"\nFIESC specializations in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<70} {'Short Name':<15} {'Faculty':<30}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<70} {row[2]:<15} {row[3]:<30}")
            
            print("-" * 80)
            
            # List all faculties
            result = conn.execute(text(
                """
                SELECT id, name, short_name
                FROM faculties
                ORDER BY id
                """
            ))
            faculties = result.fetchall()
            
            print(f"\nAll faculties in database ({len(faculties)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<70} {'Short Name':<15}")
            print("-" * 80)
            
            for faculty in faculties:
                print(f"{faculty[0]:<5} {faculty[1]:<70} {faculty[2]:<15}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding FIESC faculty and specializations: {e}")

if __name__ == "__main__":
    add_fiesc_faculty_and_specializations()
