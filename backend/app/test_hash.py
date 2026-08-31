from app.core.security import hash_password, verify_password

password = "admin123"

hashed = hash_password(password)

print("Original Password :", password)
print("Hashed Password   :", hashed)

result = verify_password(password, hashed)

print("Password Match :", result)