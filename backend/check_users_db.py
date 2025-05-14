"""
Script to check users in the database
"""
from app.db.base import get_db
from sqlalchemy import text

def main():
    # Get database connection
    db = next(get_db())
    
    # Check users table columns
    print("USERS TABLE COLUMNS:")
    columns_query = text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'")
    columns = db.execute(columns_query).fetchall()
    for column in columns:
        print(f"- {column[0]}")
    
    # Check users data
    print("\nUSERS DATA:")
    users_query = text("SELECT id, name, email, role FROM users LIMIT 10")
    users = db.execute(users_query).fetchall()
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")
    
    # Create a test user if none exists
    if not users:
        print("\nNo users found. Creating a test user...")
        from app.core.security import get_password_hash
        
        # Create a secretariat user
        create_secretariat_query = text("""
            INSERT INTO users (name, email, password, role)
            VALUES (:name, :email, :password, :role)
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """)
        
        secretariat_result = db.execute(create_secretariat_query, {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": get_password_hash("password123"),
            "role": "SECRETARIAT"
        })
        db.commit()
        
        # Create a professor user
        create_professor_query = text("""
            INSERT INTO users (name, email, password, role)
            VALUES (:name, :email, :password, :role)
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """)
        
        professor_result = db.execute(create_professor_query, {
            "name": "John Smith",
            "email": "professor@example.com",
            "password": get_password_hash("password123"),
            "role": "PROFESSOR"
        })
        db.commit()
        
        # Create a student user
        create_student_query = text("""
            INSERT INTO users (name, email, password, role)
            VALUES (:name, :email, :password, :role)
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """)
        
        student_result = db.execute(create_student_query, {
            "name": "Student User",
            "email": "student@example.com",
            "password": get_password_hash("password123"),
            "role": "STUDENT"
        })
        db.commit()
        
        print("Test users created. You can now log in with:")
        print("Admin: admin@example.com / password123")
        print("Professor: professor@example.com / password123")
        print("Student: student@example.com / password123")
        
        # Check users again
        print("\nUSERS DATA AFTER CREATION:")
        users = db.execute(users_query).fetchall()
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")

if __name__ == "__main__":
    main()
