import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "exam_planning_db")  # Use the container name
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")

# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Connect to the database
    with engine.connect() as connection:
        # Query users table
        result = connection.execute(text("SELECT * FROM users"))
        
        # Print user information
        print("\n=== Available Users ===")
        print(f"{'ID':<5} {'Email':<30} {'Name':<30} {'Role':<15}")
        print("-" * 80)
        
        for row in result:
            print(f"{row.id:<5} {row.email:<30} {row.name:<30} {row.role:<15}")
        
        print("\nNote: All users have the password 'password' unless otherwise specified.")
        print("To log in, use the email address and password.")
        
except Exception as e:
    print(f"Error connecting to the database: {e}")
    sys.exit(1)
