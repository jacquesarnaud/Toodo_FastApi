from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(claire:str , hash:str) -> bool:
    return pwd_context.verify(claire,hash)