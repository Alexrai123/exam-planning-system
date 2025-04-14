from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/exam_planning")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Execute a simple query to check connection
    print("Checking database connection...")
    result = db.execute(text("SELECT 1")).scalar()
    print(f"Database connection successful: {result}")
    
    # Check if users table exists
    print("\nChecking users table...")
    result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")).scalar()
    print(f"Users table exists: {result}")
    
    # Get users table structure
    print("\nUsers table structure:")
    columns = db.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'users'
        ORDER BY ordinal_position
    """)).fetchall()
    for column in columns:
        print(f"  {column[0]}: {column[1]} (nullable: {column[2]})")
    
    # Check user data
    print("\nUsers in database:")
    users = db.execute(text("SELECT id, name, email, role FROM users")).fetchall()
    for user in users:
        print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")
    
    # Check enum types
    print("\nEnum types in database:")
    enums = db.execute(text("""
        SELECT t.typname, e.enumlabel
        FROM pg_type t
        JOIN pg_enum e ON e.enumtypid = t.oid
        ORDER BY t.typname, e.enumsortorder
    """)).fetchall()
    current_enum = None
    for enum in enums:
        if enum[0] != current_enum:
            current_enum = enum[0]
            print(f"  {current_enum}:")
        print(f"    - {enum[1]}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
