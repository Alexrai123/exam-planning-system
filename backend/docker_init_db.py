from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash

# Database connection string
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/exam_planning"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    db = SessionLocal()
    
    try:
        # Create users table if it doesn't exist
        db.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            role VARCHAR(50) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE
        )
        """))
        
        # Check if we already have users
        result = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        
        if result == 0:
            print("Creating initial admin user...")
            
            # Create admin user
            hashed_password = get_password_hash("password")
            db.execute(
                text("""
                INSERT INTO users (email, password, full_name, role, is_active) 
                VALUES (:email, :password, :full_name, :role, :is_active)
                """),
                {
                    "email": "admin@example.com",
                    "password": hashed_password,
                    "full_name": "Admin User",
                    "role": "secretariat",
                    "is_active": True
                }
            )
            
            print("Admin user created successfully!")
        else:
            print("Users already exist in the database, skipping initialization.")
        
        db.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing the PostgreSQL database...")
    init_db()
    print("Database initialization completed!")
