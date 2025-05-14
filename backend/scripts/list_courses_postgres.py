"""
Script to list all courses in the database using PostgreSQL
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.base import engine

def list_all_courses():
    """
    List all courses in the database using PostgreSQL
    """
    try:
        with engine.connect() as conn:
            # Get table names from PostgreSQL
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            tables = [row[0] for row in result]
            print(f"Tables in database: {', '.join(tables)}")
            
            # Try to query courses table
            if 'courses' in tables:
                result = conn.execute(text("SELECT id, name, profesor_name FROM courses"))
                rows = result.fetchall()
                print(f"\nFound {len(rows)} courses in the database:")
                print("-" * 80)
                print(f"{'ID':<5} {'Name':<40} {'Professor':<30}")
                print("-" * 80)
                for row in rows:
                    print(f"{row[0]:<5} {row[1]:<40} {row[2] or 'N/A':<30}")
                print("-" * 80)
            else:
                print("\nCourses table not found. Checking other possible table names...")
                
                # Try alternative table names
                for table in tables:
                    if 'course' in table.lower():
                        print(f"\nTrying table: {table}")
                        try:
                            # Get column names
                            result = conn.execute(text(
                                f"SELECT column_name FROM information_schema.columns "
                                f"WHERE table_name = '{table}'"
                            ))
                            columns = [row[0] for row in result]
                            print(f"Columns: {', '.join(columns)}")
                            
                            # Check if the table has name and profesor_name columns
                            if 'name' in columns:
                                query = f"SELECT id, name"
                                if 'profesor_name' in columns:
                                    query += ", profesor_name"
                                else:
                                    query += ", NULL as profesor_name"
                                query += f" FROM {table}"
                                
                                result = conn.execute(text(query))
                                rows = result.fetchall()
                                print(f"\nFound {len(rows)} records in {table}:")
                                print("-" * 80)
                                print(f"{'ID':<5} {'Name':<40} {'Professor':<30}")
                                print("-" * 80)
                                for row in rows:
                                    print(f"{row[0]:<5} {row[1]:<40} {row[2] or 'N/A':<30}")
                                print("-" * 80)
                        except Exception as e:
                            print(f"Error querying {table}: {e}")
    except Exception as e:
        print(f"Error accessing database: {e}")

if __name__ == "__main__":
    list_all_courses()
