import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters - try both localhost and container name
hosts = ["localhost", "exam_planning_db"]
connected = False

for host in hosts:
    try:
        # Database connection parameters
        DB_USER = "postgres"
        DB_PASSWORD = "postgres"
        DB_HOST = host
        DB_PORT = "5432"
        DB_NAME = "postgres"

        # Create database URL
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        print(f"Trying to connect to database at {DB_HOST}...")
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Connect to the database
        with engine.connect() as connection:
            # First, check what tables exist
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = connection.execute(tables_query).fetchall()
            
            print(f"Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Query users table
            if 'users' in [t[0] for t in tables]:
                result = connection.execute(text("SELECT id, name, email, role, password FROM users"))
                
                # Print user information
                print("\n=== Available Users ===")
                print(f"{'ID':<5} {'Email':<30} {'Name':<30} {'Role':<15}")
                print("-" * 80)
                
                for row in result:
                    print(f"{row.id:<5} {row.email:<30} {row.name:<30} {row.role:<15}")
                
                print("\nNote: All users have the password 'password' unless otherwise specified.")
                print("To log in, use the email address and password.")
            else:
                print("\nNo 'users' table found.")
            
            connected = True
            break
            
    except Exception as e:
        print(f"Error connecting to {host}: {e}")

if not connected:
    print("Could not connect to the database using any of the configured hosts.")
    sys.exit(1)
