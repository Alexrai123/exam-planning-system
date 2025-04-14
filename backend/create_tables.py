from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import sys

# Add the backend directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import models after adding to path
from app.db.base import Base
from app.models.user import User
from app.models.course import Course
from app.models.sala import Sala
from app.models.grupa import Grupa
from app.models.exam import Exam

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/exam_planning")

def create_tables():
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("Database tables created successfully!")
        
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == "__main__":
    create_tables()
