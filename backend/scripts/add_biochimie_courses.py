"""
Script to add Biochimie (Biochemistry) courses to the database
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
    Add Biochimie (Biochemistry) courses to the database
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
                "SELECT id, name, short_name FROM specializations WHERE short_name = 'BIO' OR name LIKE '%Biochimie%'"
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
                {"name": "Introducere in studiul celulei. Celula: unitate structurala si functionala fundamentala a vietii", "year": 1, "semester": 1},
                {"name": "Teoria celulara: momente, etape, evolutie", "year": 1, "semester": 1},
                {"name": "Celula procariota-celula eucariota. Organizarea celulelor procariote", "year": 1, "semester": 1},
                {"name": "Organizarea celulelor eucariote. Compartimentarea celulara", "year": 1, "semester": 1},
                {"name": "Membrana celulara: structura si functii generale", "year": 1, "semester": 1},
                {"name": "Modelul mozaicului fluid al organizarii membranelor celulare", "year": 1, "semester": 1},
                {"name": "Transportul prin membrane (macromolecule si particule)", "year": 1, "semester": 2},
                {"name": "Exocitoza, endocitoza si transcitoza. Fagocitoza", "year": 1, "semester": 2},
                {"name": "Junctiunile celulare: structura si functii. Plasmalema", "year": 1, "semester": 2},
                {"name": "Sistemul endomembranar al celulei. Structura si functiile reticulului endoplasmatic", "year": 1, "semester": 2},
                {"name": "Structura si functiile complexului Golgi si lizozomilor", "year": 1, "semester": 2},
                {"name": "Polaritatea subcompartimentelor golgiene", "year": 1, "semester": 2},
                {"name": "Organitele de conversie energetica. Structura si functiile mitocondriilor", "year": 1, "semester": 2},
                {"name": "Citoscheletul celulelor eucariote", "year": 1, "semester": 2},
                {"name": "Structura si functiile microtubulilor", "year": 1, "semester": 2},
                {"name": "Diviziunea celulara la procariote si eucariote", "year": 1, "semester": 2},
                {"name": "Matricea extracelulara: componente si functii", "year": 1, "semester": 2},
                {"name": "Evolutia la nivel celular: originea si evolutia compartimentelor celulare la eucariote", "year": 1, "semester": 2}
            ]
            
            # Define Biochimie Year 2 courses from the second image
            biochimie_year2_courses = [
                {"name": "Etapele dezvoltarii zoologiei: Clasificarea organismelor vii", "year": 2, "semester": 1},
                {"name": "Nomenclatura binara si codul de clasificare", "year": 2, "semester": 1},
                {"name": "Nomenclatura Zoologica, Tipuri de caractere folosite in clasificare", "year": 2, "semester": 1},
                {"name": "Regnul Protista-caractere generale clasificare, biologie", "year": 2, "semester": 1},
                {"name": "Regnul Animalia-caractere generale, etapele dezvoltarii embrionare la metazoare", "year": 2, "semester": 1},
                {"name": "Ramuri evolutive majore ale metazoarelor", "year": 2, "semester": 1},
                {"name": "Radial Diploblastica: Phylum Porifera-caractere generale, clasificare, exemple, originea porospongierelor", "year": 2, "semester": 1},
                {"name": "Phylum Cnidaria-caractere generale, clasificare, exemple, originea si evolutia cnidarilor", "year": 2, "semester": 1},
                {"name": "Bilateria Triploblastica: Phylum Platyhelminthes-caractere generale, clasificare, exemple, origine", "year": 2, "semester": 1},
                {"name": "Aschelminthes-caractere generale, clasificare, exemple, originea si evolutia nematodelor", "year": 2, "semester": 2},
                {"name": "Phylum Mollusca-caractere generale, clasificare, exemple, originea si evolutia molustelor", "year": 2, "semester": 2},
                {"name": "Phylum Annelida-caractere generale, clasificare, exemple, originea si evolutia anelidelor", "year": 2, "semester": 2},
                {"name": "Phylum Arthropoda-caractere generale, clasificare, exemple, originea si evolutia artropodelor", "year": 2, "semester": 2},
                {"name": "Clasa Arachnida si Insecta-caractere generale, clasificare, exemple, originea si evolutia artropodelor", "year": 2, "semester": 2},
                {"name": "Phylum Echinodermata-caractere generale, clasificare, exemple, originea si evolutia echinodermelor", "year": 2, "semester": 2},
                {"name": "Phylum Chordata-caractere generale, clasificare, exemple, originea si evolutia cordatelor", "year": 2, "semester": 2},
                {"name": "Subphylum Vertebrata-caractere generale, clasificare, exemple, originea si evolutia vertebratelor", "year": 2, "semester": 2},
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
                {"name": "Introducere in tematica cursului. Structura si functiile acizilor nucleici si proteinelor", "year": 3, "semester": 1},
                {"name": "Introducere in metabolism", "year": 3, "semester": 1},
                {"name": "Biosinteza aminoacizilor ne-esentiali si esentiali", "year": 3, "semester": 1},
                {"name": "Dezaminarea si ciclul ureogenetic (Krebs-Henseleit)", "year": 3, "semester": 1},
                {"name": "Transaminarea. Degradarea aminoacizilor", "year": 3, "semester": 1},
                {"name": "Aminoacizii ca precursori biosintetici: biosinteza si degradarea hemului", "year": 3, "semester": 1},
                {"name": "Biosinteza aminelor active din punct de vedere fiziologic", "year": 3, "semester": 1},
                {"name": "Biosinteza peptidelor cu rol biologic", "year": 3, "semester": 2},
                {"name": "Biosinteza si modificarile post-translationale ale proteinelor", "year": 3, "semester": 2},
                {"name": "Degradarea proteinelor la nivel celular", "year": 3, "semester": 2},
                {"name": "Digestia proteinelor si absorbtia aminoacizilor", "year": 3, "semester": 2},
                {"name": "Interrelatii intre metabolismul proteic si cel al acizilor nucleici", "year": 3, "semester": 2},
                {"name": "Turn-overul proteic si reglarea transcriptiei si a translatiei din punct de vedere metabolic", "year": 3, "semester": 2},
                {"name": "Degradarea nucleotidelor purinice si pirimidinice", "year": 3, "semester": 2},
                {"name": "Coagularea sangelui. Hemostaza si fibrinoliza", "year": 3, "semester": 2},
                {"name": "Enzime si hormoni implicati in metabolismul acizilor nucleici si proteinelor", "year": 3, "semester": 2},
                {"name": "Integrarea metabolismului glucidelor si lipidelor cu metabolismul proteinelor si acizilor nucleici", "year": 3, "semester": 2}
            ]
            
            # Combine all courses
            all_biochimie_courses = biochimie_year1_courses + biochimie_year2_courses + biochimie_year3_courses
            
            # Add courses
            courses_added = 0
            print("\nAdding Biochimie courses to the database...")
            print("-" * 80)
            
            for course in all_biochimie_courses:
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
