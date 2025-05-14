"""
Migration script to add professor_id column to exams table
"""
import os
import sys
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get the absolute path to the app.db file
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(script_dir))
db_path = os.path.join(backend_dir, 'app.db')

# Database connection
DATABASE_URL = f"sqlite:///{db_path}"
print(f"Using database at: {db_path}")

def run_migration():
    """Add professor_id column to exams table using direct SQLite connection"""
    try:
        # Connect directly to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(exams)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'professor_id' not in columns:
            print("Adding professor_id column to exams table...")
            cursor.execute("ALTER TABLE exams ADD COLUMN professor_id INTEGER REFERENCES users(id)")
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("Column professor_id already exists in exams table.")
        
        conn.close()
        return True
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        return False

if __name__ == "__main__":
    run_migration()
