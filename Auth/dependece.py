from fastapi import HTTPException,status,Depends
from models.models import ModelUser
from database.database import db_dependency
from Auth.jwtoken import decode_token
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Auth/login")

async def get_curent_user(db : db_dependency,token: Annotated[str,Depends(oauth2_scheme)] )->ModelUser:
    paylod = decode_token(token)
    if not paylod:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token invalide")
    user_id = paylod.get("sub")
    db_user = db.query(ModelUser).filter(ModelUser.id == int(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Utilisateur introuvable')
    return db_user

curent_dependancy=Annotated[ModelUser,Depends(get_curent_user)]