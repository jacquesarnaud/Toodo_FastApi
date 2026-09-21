from fastapi import APIRouter,Body,HTTPException
from starlette import status
from database.database import db_dependency
from models.models import ModelUser
from typing import Annotated
from shemas.user_register import User_create
from Auth.hashing import hash_password,verify_password
from shemas.user_login import User_log
from Auth.jwtoken import create_access_token


router_auth = APIRouter(prefix="/Auth" , tags=["Authentification"])


@router_auth.post("/register", status_code=status.HTTP_201_CREATED)
async def register (register_user:Annotated[User_create,Body()],db:db_dependency):
    register_user.password = hash_password(register_user.password)
    new_user= ModelUser(name=register_user.name,email=register_user.email,password=register_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"user create with succes"}

@router_auth.post("/login", status_code=status.HTTP_200_OK)
async def login (login_user:Annotated[User_log,Body()],db:db_dependency):
    
    db_user = db.query(ModelUser).filter(ModelUser.email == login_user.email).first()
    if not db_user or not verify_password(login_user.password , db_user.password):
        raise HTTPException(status_code=401,detail="identication invalide")

    acess_token = create_access_token({"sub":str(db_user.id), "type":"access"})

    return {"access_token":acess_token}

