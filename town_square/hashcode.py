
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """check if inpututed and saved passwrod are equal"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """hash a pasword"""
    return pwd_context.hash(password)
