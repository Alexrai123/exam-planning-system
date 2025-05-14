"""
Migration script to add professor_id field to the exams table.
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
    """Add professor_id column to the exams table."""
    with engine.connect() as connection:
        # Begin transaction
        trans = connection.begin()
        try:
            # Check if professor_id column exists
            check_professor_id = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'exams' AND column_name = 'professor_id'
            """)
            
            professor_id_exists = connection.execute(check_professor_id).fetchone()
            
            # Add professor_id column if it doesn't exist
            if not professor_id_exists:
                print("Adding professor_id column to exams table...")
                add_professor_id = text("""
                    ALTER TABLE exams
                    ADD COLUMN professor_id INTEGER REFERENCES users(id)
                """)
                connection.execute(add_professor_id)
                print("professor_id column added successfully.")
            else:
                print("professor_id column already exists.")
            
            # Commit transaction
            trans.commit()
            print("Migration completed successfully.")
            
        except Exception as e:
            # Rollback transaction in case of error
            trans.rollback()
            print(f"Error during migration: {e}")
            sys.exit(1)

if __name__ == "__main__":
    print("Running migration to add professor_id column...")
    run_migration()
    print("Done")
