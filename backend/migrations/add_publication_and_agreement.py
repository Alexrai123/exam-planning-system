"""
Migration script to add publication_date and professor_agreement fields to the exams table.
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Database connection parameters for Docker environment
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "exam_planning_db"  # Use the Docker container name as the host
DB_PORT = "5432"
DB_NAME = "exam_planning"

# Create database connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def run_migration():
    """Add publication_date and professor_agreement columns to the exams table."""
    with engine.connect() as connection:
        # Begin transaction
        trans = connection.begin()
        try:
            # Check if publication_date column exists
            check_publication_date = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'exams' AND column_name = 'publication_date'
            """)
            
            publication_date_exists = connection.execute(check_publication_date).fetchone()
            
            # Check if professor_agreement column exists
            check_professor_agreement = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'exams' AND column_name = 'professor_agreement'
            """)
            
            professor_agreement_exists = connection.execute(check_professor_agreement).fetchone()
            
            # Add publication_date column if it doesn't exist
            if not publication_date_exists:
                print("Adding publication_date column to exams table...")
                add_publication_date = text("""
                    ALTER TABLE exams
                    ADD COLUMN publication_date TIMESTAMP
                """)
                connection.execute(add_publication_date)
                print("publication_date column added successfully")
            else:
                print("publication_date column already exists")
            
            # Add professor_agreement column if it doesn't exist
            if not professor_agreement_exists:
                print("Adding professor_agreement column to exams table...")
                add_professor_agreement = text("""
                    ALTER TABLE exams
                    ADD COLUMN professor_agreement BOOLEAN NOT NULL DEFAULT FALSE
                """)
                connection.execute(add_professor_agreement)
                print("professor_agreement column added successfully")
            else:
                print("professor_agreement column already exists")
            
            # Commit the transaction
            trans.commit()
            print("Migration completed successfully")
            
        except Exception as e:
            # Rollback in case of error
            trans.rollback()
            print(f"Error: {e}")
            print("Migration failed, changes rolled back")
            sys.exit(1)

if __name__ == "__main__":
    print("Running migration to add publication_date and professor_agreement columns...")
    run_migration()
    print("Done")
