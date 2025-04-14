from passlib.context import CryptContext

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# The stored hash from the database
stored_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

# The password to verify
password = "password"

# Verify the password
is_valid = pwd_context.verify(password, stored_hash)

print(f"Password 'password' matches the stored hash: {is_valid}")

# If the password doesn't match, let's try some other common passwords
if not is_valid:
    common_passwords = ["admin", "admin123", "secretariat", "12345678", "password123"]
    for test_password in common_passwords:
        is_valid = pwd_context.verify(test_password, stored_hash)
        if is_valid:
            print(f"Password '{test_password}' matches the stored hash: {is_valid}")
            break
    else:
        print("None of the common passwords match the stored hash.")
