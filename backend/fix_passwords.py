"""
Script to fix user passwords in the database
"""
from app.db.base import get_db
from app.core.security import get_password_hash
from sqlalchemy import text

def main():
    # Get database connection
    db = next(get_db())
    
    # Get all users
    print("Fetching users...")
    users_query = text("SELECT id, email FROM users")
    users = db.execute(users_query).fetchall()
    
    if not users:
        print("No users found in the database.")
        return
    
    print(f"Found {len(users)} users.")
    
    # Update passwords with proper bcrypt hashes
    for user in users:
        user_id = user[0]
        email = user[1]
        
        # Generate a proper bcrypt hash for 'password123'
        password_hash = get_password_hash("password123")
        
        # Update the user's password
        update_query = text("""
            UPDATE users 
            SET password = :password_hash 
            WHERE id = :user_id
        """)
        
        try:
            db.execute(update_query, {
                "password_hash": password_hash,
                "user_id": user_id
            })
            db.commit()
            print(f"Updated password for user {email} (ID: {user_id})")
        except Exception as e:
            db.rollback()
            print(f"Error updating password for user {email}: {str(e)}")
    
    print("\nAll passwords have been updated to 'password123'.")
    print("You can now log in with any user account using the password 'password123'.")

if __name__ == "__main__":
    main()
