from jose import jwt,JWTError
from datetime import datetime,timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN = 5

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def decode_token(token:str):
    try:
        paylod  = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return paylod
    except JWTError:
        return None