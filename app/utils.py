from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Create the PasswordHasher instance
ph = PasswordHasher()

def hash(password: str) -> str:
    return ph.hash(password)

def verify(plain_password: str, hashed_password:str) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    
