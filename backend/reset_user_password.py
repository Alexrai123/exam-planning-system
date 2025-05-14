"""
Script to reset a user's password
"""
from app.db.base import get_db
from app.core.security import get_password_hash
from sqlalchemy import text
import sys

def reset_user_password(email, new_password):
    # Get database connection
    db = next(get_db())
    
    # First check if the user exists
    check_query = text("SELECT id, name, role FROM users WHERE email = :email")
    user = db.execute(check_query, {"email": email}).fetchone()
    
    if not user:
        print(f"No user found with email: {email}")
        return False
    
    # Hash the new password
    hashed_password = get_password_hash(new_password)
    
    # Update the user's password
    update_query = text("""
        UPDATE users 
        SET password = :password
        WHERE email = :email
        RETURNING id
    """)
    
    result = db.execute(update_query, {
        "email": email,
        "password": hashed_password
    })
    
    # Commit the transaction
    db.commit()
    
    updated_id = result.fetchone()
    
    if updated_id:
        print(f"\nPassword reset successful for:")
        print(f"User: {user[1]} (ID: {user[0]})")
        print(f"Email: {email}")
        print(f"Role: {user[2]}")
        print(f"New password: {new_password}")
        return True
    else:
        print("Password reset failed.")
        return False

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        new_password = sys.argv[2]
    else:
        email = input("Enter the email of the user: ")
        new_password = input("Enter the new password: ")
    
    reset_user_password(email, new_password)
