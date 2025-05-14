"""
Script to update FMSB specialization short names
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def update_specialization_shortnames():
    """
    Update short names for FMSB specializations to make them more distinct
    """
    try:
        # Define improved short names
        improved_shortnames = {
            "Medicina": "Med",
            "Asistenta medicala generala": "AMG",
            "Balneofiziokinetoterapie si recuperare": "BFKT",
            "Biochimie": "Bioc",
            "Biologie": "Biol",
            "Nutritie si dietetica": "NutD",
            "Tehnica dentara": "TehD",
            "Master - Nutritie si Recuperare Medicala": "MNRM"
        }
        
        # Update short names in the database
        with engine.connect() as conn:
            print("Updating specialization short names:")
            print("-" * 80)
            
            for name, short_name in improved_shortnames.items():
                conn.execute(text(
                    "UPDATE specializations SET short_name = :short_name WHERE name = :name"
                ), {"name": name, "short_name": short_name})
                
                print(f"Updated: {name} -> {short_name}")
            
            conn.commit()
            print("-" * 80)
            
            # List all specializations with updated short names
            result = conn.execute(text(
                "SELECT id, name, faculty_id, short_name FROM specializations WHERE faculty_id = '21' ORDER BY id"
            ))
            rows = result.fetchall()
            
            print(f"\nFMSB Specializations with updated short names ({len(rows)}):")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<50} {'Short Name':<15}")
            print("-" * 80)
            
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<50} {row[3]:<15}")
            
            print("-" * 80)
            print("\nSpecialization short names updated successfully.")
        
    except Exception as e:
        print(f"Error updating specialization short names: {e}")

if __name__ == "__main__":
    update_specialization_shortnames()
