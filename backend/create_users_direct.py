"""
Script to create test accounts for professor and admin roles using direct SQL
"""
import os
import sys
from sqlalchemy import create_engine, text
from app.core.security import get_password_hash

# Database connection parameters
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"  # Use localhost for direct connection
DB_PORT = "5432"
DB_NAME = "exam_planning"

# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_test_accounts():
    """Create test accounts for professor and admin roles"""
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Connect to the database
        with engine.connect() as connection:
            # Begin transaction
            trans = connection.begin()
            
            try:
                # Create professor user
                professor_email = "john.smith@usv.ro"
                
                # Check if professor user already exists
                check_professor_query = text("""
                    SELECT id FROM users WHERE email = :email
                """)
                
                result = connection.execute(check_professor_query, {"email": professor_email})
                professor_user = result.fetchone()
                
                if not professor_user:
                    print(f"Creating professor user with email: {professor_email}")
                    # Create password hash
                    password_hash = get_password_hash("password123")
                    
                    # Insert professor user
                    insert_user_query = text("""
                        INSERT INTO users (name, email, password, role)
                        VALUES (:name, :email, :password, :role)
                        RETURNING id
                    """)
                    
                    result = connection.execute(insert_user_query, {
                        "name": "John Smith",
                        "email": professor_email,
                        "password": password_hash,
                        "role": "PROFESSOR"
                    })
                    
                    professor_id = result.fetchone()[0]
                    print(f"Professor user created with ID: {professor_id}")
                    
                    # Check if professor exists in professors table
                    check_professor_record_query = text("""
                        SELECT name FROM professors WHERE name = :name
                    """)
                    
                    result = connection.execute(check_professor_record_query, {"name": "John Smith"})
                    professor_record = result.fetchone()
                    
                    if not professor_record:
                        # Create professor record
                        insert_professor_query = text("""
                            INSERT INTO professors (name, specialization, title, email, user_id)
                            VALUES (:name, :specialization, :title, :email, :user_id)
                        """)
                        
                        connection.execute(insert_professor_query, {
                            "name": "John Smith",
                            "specialization": "Computer Science",
                            "title": "PhD",
                            "email": professor_email,
                            "user_id": professor_id
                        })
                        
                        print("Professor record created")
                    else:
                        # Update professor record with user_id
                        update_professor_query = text("""
                            UPDATE professors
                            SET email = :email, user_id = :user_id
                            WHERE name = :name
                        """)
                        
                        connection.execute(update_professor_query, {
                            "email": professor_email,
                            "user_id": professor_id,
                            "name": "John Smith"
                        })
                        
                        print("Existing professor record updated")
                else:
                    print(f"Professor user already exists with ID: {professor_user[0]}")
                
                # Create admin user
                admin_email = "admin@usv.ro"
                
                # Check if admin user already exists
                check_admin_query = text("""
                    SELECT id FROM users WHERE email = :email
                """)
                
                result = connection.execute(check_admin_query, {"email": admin_email})
                admin_user = result.fetchone()
                
                if not admin_user:
                    print(f"Creating admin user with email: {admin_email}")
                    # Create password hash
                    password_hash = get_password_hash("password123")
                    
                    # Insert admin user
                    insert_admin_query = text("""
                        INSERT INTO users (name, email, password, role)
                        VALUES (:name, :email, :password, :role)
                        RETURNING id
                    """)
                    
                    result = connection.execute(insert_admin_query, {
                        "name": "Admin User",
                        "email": admin_email,
                        "password": password_hash,
                        "role": "ADMIN"
                    })
                    
                    admin_id = result.fetchone()[0]
                    print(f"Admin user created with ID: {admin_id}")
                else:
                    print(f"Admin user already exists with ID: {admin_user[0]}")
                
                # Commit transaction
                trans.commit()
                print("All accounts created successfully!")
                
            except Exception as e:
                # Rollback transaction on error
                trans.rollback()
                print(f"Error in database transaction: {str(e)}")
                sys.exit(1)
    
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    from app.core.security import get_password_hash
    create_test_accounts()
