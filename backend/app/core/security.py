from passlib.context import CryptContext

# Create password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Convert plain password into hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Verify password during login
    """
    return pwd_context.verify(plain_password, hashed_password)