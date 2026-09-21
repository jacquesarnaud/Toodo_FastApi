from fastapi.security.api_key import APIKeyHeader
from fastapi import Security,HTTPException
from models.models import ModelUser
from database.database import db_dependency
from Auth.jwtoken import decode_token

api_key_hearder = APIKeyHeader(name="Authorization")


def get_curent_user(db : db_dependency,token: str = Security(api_key_hearder))->ModelUser:
    paylod = decode_token(token)
    if not paylod:
        raise HTTPException(status_code=401,detail="token invalide")
    user_id = paylod.get("sub")
    db_user = db.query(ModelUser).filter(ModelUser.id == int(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=401,detail='Utilisateur introuvable')
    return db_user

