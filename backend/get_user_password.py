"""
Script to retrieve user information for a specific email
"""
from app.db.base import get_db
from sqlalchemy import text
import sys

def get_user_by_email(email):
    # Get database connection
    db = next(get_db())
    
    # Query user data
    user_query = text("SELECT id, name, email, password, role FROM users WHERE email = :email")
    user = db.execute(user_query, {"email": email}).fetchone()
    
    if user:
        print(f"\nUSER FOUND:")
        print(f"ID: {user[0]}")
        print(f"Name: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"Password Hash: {user[3]}")
        print(f"Role: {user[4]}")
        print("\nNote: This is the hashed password, not the plaintext password.")
        print("For security reasons, passwords are stored as hashes and cannot be directly decrypted.")
    else:
        print(f"\nNo user found with email: {email}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Enter the email to search for: ")
    
    get_user_by_email(email)
