"""
Script to add FEEA (Facultatea de Economie si Administrarea Afacerilor) specializations to the database
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_feea_specializations():
    """
    Add FEEA (Facultatea de Economie si Administrarea Afacerilor) specializations to the database
    """
    try:
        with engine.connect() as conn:
            # Check if FEEA faculty exists, create if needed
            result = conn.execute(text(
                "SELECT id, name, short_name FROM faculties WHERE short_name = 'FEEA'"
            ))
            feea_faculty = result.fetchone()
            
            if feea_faculty:
                print(f"Found FEEA faculty with ID: {feea_faculty[0]}, Name: {feea_faculty[1]}, Short Name: {feea_faculty[2]}")
                feea_id = feea_faculty[0]
            else:
                print("FEEA faculty not found, creating it...")
                conn.execute(text(
                    """
                    INSERT INTO faculties (id, name, short_name)
                    VALUES ('22', 'Facultatea de Economie si Administrarea Afacerilor', 'FEEA')
                    """
                ))
                conn.commit()
                
                result = conn.execute(text(
                    "SELECT id, name, short_name FROM faculties WHERE short_name = 'FEEA'"
                ))
                feea_faculty = result.fetchone()
                print(f"Created FEEA faculty with ID: {feea_faculty[0]}, Name: {feea_faculty[1]}, Short Name: {feea_faculty[2]}")
                feea_id = feea_faculty[0]
            
            # Define FEEA specializations from the provided image
            feea_specializations = [
                {"name": "Administrarea Afacerilor", "short_name": "AA"},
                {"name": "Afaceri Internationale", "short_name": "AI"},
                {"name": "Asistenta Manageriala si Administrativa", "short_name": "AMA"},
                {"name": "Contabilitate si Informatica de Gestiune", "short_name": "CIG"},
                {"name": "Economia Comertului, Turismului si Serviciilor", "short_name": "ECTS"},
                {"name": "Economia Generala si Comunicare Economica", "short_name": "EGCE"},
                {"name": "Finante si Banci", "short_name": "FB"},
                {"name": "Informatica Economica", "short_name": "IE"},
                {"name": "Management", "short_name": "MNG"}
            ]
            
            # Add specializations
            specializations_added = 0
            print("\nAdding FEEA specializations to the database...")
            print("-" * 80)
            
            for spec in feea_specializations:
                # Check if specialization already exists
                result = conn.execute(text(
                    "SELECT id FROM specializations WHERE name = :name AND faculty_id = :faculty_id"
                ), {"name": spec["name"], "faculty_id": feea_id})
                
                if result.rowcount == 0:
                    # Add specialization
                    conn.execute(text(
                        """
                        INSERT INTO specializations (name, short_name, faculty_id)
                        VALUES (:name, :short_name, :faculty_id)
                        """
                    ), {
                        "name": spec["name"],
                        "short_name": spec["short_name"],
                        "faculty_id": feea_id
                    })
                    
                    specializations_added += 1
                    print(f"Added: {spec['name']} ({spec['short_name']})")
                else:
                    print(f"Specialization already exists: {spec['name']}")
            
            conn.commit()
            print("-" * 80)
            print(f"Added {specializations_added} new FEEA specializations to the database")
            
            # List all FEEA specializations
            result = conn.execute(text(
                """
                SELECT s.id, s.name, s.short_name, f.name as faculty_name
                FROM specializations s
                JOIN faculties f ON s.faculty_id = f.id
                WHERE s.faculty_id = :faculty_id
                ORDER BY s.name
                """
            ), {"faculty_id": feea_id})
            rows = result.fetchall()
            
            print(f"\nFEEA specializations in database ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Short Name':<15} {'Faculty':<30}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<50} {row[2]:<15} {row[3]:<30}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding FEEA specializations: {e}")

if __name__ == "__main__":
    add_feea_specializations()
