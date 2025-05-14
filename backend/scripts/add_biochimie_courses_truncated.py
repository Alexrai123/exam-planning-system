"""
Script to add Biochimie (Biochemistry) courses to the database with truncated names
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def add_biochimie_courses():
    """
    Add Biochimie (Biochemistry) courses to the database with truncated names
    """
    try:
        with engine.connect() as conn:
            # Check if N/A professor exists, create if needed
            placeholder = "N/A"
            result = conn.execute(text(
                "SELECT name FROM professors WHERE name = :name"
            ), {"name": placeholder})
            
            if result.rowcount == 0:
                conn.execute(text(
                    "INSERT INTO professors (name, faculty) VALUES (:name, 'N/A')"
                ), {"name": placeholder})
                print(f"Created placeholder professor: {placeholder}")
            
            # Get specialization ID for Biochimie
            result = conn.execute(text(
                "SELECT id, name, short_name FROM specializations WHERE short_name = 'Bioc' OR name LIKE '%Biochimie%'"
            ))
            bio_spec = result.fetchone()
            
            if bio_spec:
                print(f"Found Biochimie specialization with ID: {bio_spec[0]}, Name: {bio_spec[1]}, Short Name: {bio_spec[2]}")
                bio_spec_id = bio_spec[0]
            else:
                print("Biochimie specialization not found, creating it...")
                conn.execute(text(
                    """
                    INSERT INTO specializations (name, short_name, faculty_id)
                    VALUES ('Biochimie', 'BIO', '21')
                    """
                ))
                conn.commit()
                
                result = conn.execute(text(
                    "SELECT id, name, short_name FROM specializations WHERE short_name = 'BIO'"
                ))
                bio_spec = result.fetchone()
                print(f"Created Biochimie specialization with ID: {bio_spec[0]}, Name: {bio_spec[1]}, Short Name: {bio_spec[2]}")
                bio_spec_id = bio_spec[0]
            
            # Define Biochimie Year 1 courses from the first image
            biochimie_year1_courses = [
                {"name": "Introducere in studiul celulei", "year": 1, "semester": 1},
                {"name": "Teoria celulara: momente, etape, evolutie", "year": 1, "semester": 1},
                {"name": "Celula procariota-celula eucariota", "year": 1, "semester": 1},
                {"name": "Organizarea celulelor eucariote", "year": 1, "semester": 1},
                {"name": "Membrana celulara: structura si functii generale", "year": 1, "semester": 1},
                {"name": "Modelul mozaicului fluid al organizarii membranelor", "year": 1, "semester": 1},
                {"name": "Transportul prin membrane", "year": 1, "semester": 2},
                {"name": "Exocitoza, endocitoza si transcitoza", "year": 1, "semester": 2},
                {"name": "Junctiunile celulare: structura si functii", "year": 1, "semester": 2},
                {"name": "Sistemul endomembranar al celulei", "year": 1, "semester": 2},
                {"name": "Structura si functiile complexului Golgi si lizozomilor", "year": 1, "semester": 2},
                {"name": "Polaritatea subcompartimentelor golgiene", "year": 1, "semester": 2},
                {"name": "Organitele de conversie energetica", "year": 1, "semester": 2},
                {"name": "Citoscheletul celulelor eucariote", "year": 1, "semester": 2},
                {"name": "Structura si functiile microtubulilor", "year": 1, "semester": 2},
                {"name": "Diviziunea celulara la procariote si eucariote", "year": 1, "semester": 2},
                {"name": "Matricea extracelulara: componente si functii", "year": 1, "semester": 2},
                {"name": "Evolutia la nivel celular", "year": 1, "semester": 2}
            ]
            
            # Define Biochimie Year 2 courses from the second image
            biochimie_year2_courses = [
                {"name": "Etapele dezvoltarii zoologiei", "year": 2, "semester": 1},
                {"name": "Nomenclatura binara si codul de clasificare", "year": 2, "semester": 1},
                {"name": "Nomenclatura Zoologica", "year": 2, "semester": 1},
                {"name": "Regnul Protista-caractere generale", "year": 2, "semester": 1},
                {"name": "Regnul Animalia-caractere generale", "year": 2, "semester": 1},
                {"name": "Ramuri evolutive majore ale metazoarelor", "year": 2, "semester": 1},
                {"name": "Phylum Porifera-caractere generale", "year": 2, "semester": 1},
                {"name": "Phylum Cnidaria-caractere generale", "year": 2, "semester": 1},
                {"name": "Phylum Platyhelminthes-caractere generale", "year": 2, "semester": 1},
                {"name": "Aschelminthes-caractere generale", "year": 2, "semester": 2},
                {"name": "Phylum Mollusca-caractere generale", "year": 2, "semester": 2},
                {"name": "Phylum Annelida-caractere generale", "year": 2, "semester": 2},
                {"name": "Phylum Arthropoda-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Arachnida si Insecta-caractere generale", "year": 2, "semester": 2},
                {"name": "Phylum Echinodermata-caractere generale", "year": 2, "semester": 2},
                {"name": "Phylum Chordata-caractere generale", "year": 2, "semester": 2},
                {"name": "Subphylum Vertebrata-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Cephalaspidomorphi-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Myxini-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Chondrichthyes-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Actinopterygii-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Sarcopterygii-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Amphibia-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Reptilia-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Aves-caractere generale", "year": 2, "semester": 2},
                {"name": "Clasa Mammalia-caractere generale", "year": 2, "semester": 2}
            ]
            
            # Define Biochimie Year 3 courses from the third image
            biochimie_year3_courses = [
                {"name": "Introducere in tematica cursului", "year": 3, "semester": 1},
                {"name": "Introducere in metabolism", "year": 3, "semester": 1},
                {"name": "Biosinteza aminoacizilor ne-esentiali si esentiali", "year": 3, "semester": 1},
                {"name": "Dezaminarea si ciclul ureogenetic", "year": 3, "semester": 1},
                {"name": "Transaminarea. Degradarea aminoacizilor", "year": 3, "semester": 1},
                {"name": "Aminoacizii ca precursori biosintetici", "year": 3, "semester": 1},
                {"name": "Biosinteza aminelor active", "year": 3, "semester": 1},
                {"name": "Biosinteza peptidelor cu rol biologic", "year": 3, "semester": 2},
                {"name": "Biosinteza si modificarile post-translationale", "year": 3, "semester": 2},
                {"name": "Degradarea proteinelor la nivel celular", "year": 3, "semester": 2},
                {"name": "Digestia proteinelor si absorbtia aminoacizilor", "year": 3, "semester": 2},
                {"name": "Interrelatii intre metabolismul proteic si acizilor nucleici", "year": 3, "semester": 2},
                {"name": "Turn-overul proteic si reglarea transcriptiei", "year": 3, "semester": 2},
                {"name": "Degradarea nucleotidelor purinice si pirimidinice", "year": 3, "semester": 2},
                {"name": "Coagularea sangelui. Hemostaza si fibrinoliza", "year": 3, "semester": 2},
                {"name": "Enzime si hormoni in metabolismul acizilor nucleici", "year": 3, "semester": 2},
                {"name": "Integrarea metabolismului glucidelor si lipidelor", "year": 3, "semester": 2}
            ]
            
            # Combine all courses
            all_biochimie_courses = biochimie_year1_courses + biochimie_year2_courses + biochimie_year3_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding Biochimie courses to the database...")
            print("-" * 80)
            
            for course in all_biochimie_courses:
                # Ensure course name is not longer than 100 characters
                if len(course["name"]) > 100:
                    original_name = course["name"]
                    course["name"] = course["name"][:97] + "..."
                    print(f"Truncated course name from '{original_name}' to '{course['name']}'")
                
                # Check if course already exists
                result = conn.execute(text(
                    "SELECT id FROM courses WHERE name = :name AND faculty_id = '21'"
                ), {"name": course["name"]})
                
                if result.rowcount == 0:
                    # Add course with faculty_id 21 (FMSB) and N/A professor
                    conn.execute(text(
                        """
                        INSERT INTO courses (name, profesor_name, faculty_id, year, semester) 
                        VALUES (:name, :profesor_name, :faculty_id, :year, :semester)
                        """
                    ), {
                        "name": course["name"],
                        "profesor_name": placeholder,
                        "faculty_id": "21",
                        "year": course["year"],
                        "semester": course["semester"]
                    })
                    
                    courses_added += 1
                    print(f"Added: {course['name']} (Year {course['year']}, Semester {course['semester']})")
                else:
                    print(f"Course already exists: {course['name']}")
            
            conn.commit()
            print("-" * 80)
            print(f"Added {courses_added} new Biochimie courses to the database")
            
            # List Biochimie courses by year
            for year in range(1, 4):
                result = conn.execute(text(
                    """
                    SELECT id, name, year, semester 
                    FROM courses 
                    WHERE faculty_id = '21' AND year = :year
                    AND name IN (
                        SELECT name FROM courses 
                        WHERE name LIKE '%celul%'
                        OR name LIKE '%nucleic%'
                        OR name LIKE '%protein%'
                        OR name LIKE '%aminoaciz%'
                        OR name LIKE '%Biosintez%'
                        OR name LIKE '%Degradare%'
                        OR name LIKE '%metabolism%'
                        OR name LIKE '%Regnul%'
                        OR name LIKE '%Phylum%'
                        OR name LIKE '%Clasa%'
                        OR name LIKE '%Zoologic%'
                        OR name LIKE '%evolutia%'
                        OR name LIKE '%caractere generale%'
                    )
                    ORDER BY semester, id
                    """
                ), {"year": year})
                rows = result.fetchall()
                
                print(f"\nBiochimie Year {year} courses in database ({len(rows)}):")
                print("-" * 80)
                print(f"{'ID':<5} {'Name':<70} {'Year':<5} {'Semester':<5}")
                print("-" * 80)
                
                for row in rows:
                    print(f"{row[0]:<5} {row[1][:70]} {row[2]:<5} {row[3]:<5}")
                
                print("-" * 80)
            
            # Summary of all courses by year
            result = conn.execute(text(
                """
                SELECT year, COUNT(*) as course_count
                FROM courses 
                WHERE faculty_id = '21'
                GROUP BY year
                ORDER BY year
                """
            ))
            year_counts = result.fetchall()
            
            print(f"\nAll FMSB courses summary by year:")
            print("-" * 80)
            print(f"{'Year':<5} {'Course Count':<15}")
            print("-" * 80)
            
            for row in year_counts:
                print(f"{row[0]:<5} {row[1]:<15}")
            
            print("-" * 80)
        
    except Exception as e:
        print(f"Error adding Biochimie courses: {e}")

if __name__ == "__main__":
    add_biochimie_courses()
