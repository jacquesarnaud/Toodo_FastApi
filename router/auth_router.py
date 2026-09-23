from fastapi import APIRouter,Body,HTTPException, Depends
from starlette import status
from database.database import db_dependency
from models.models import ModelUser
from typing import Annotated
from shemas.user_register import User_create
from Auth.hashing import hash_password,verify_password
from shemas.user_login import User_log
from Auth.jwtoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

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
async def login (db:db_dependency, login_user:Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    db_user = db.query(ModelUser).filter(ModelUser.email == login_user.username).first()
    if not db_user :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect username or password")
    if not verify_password(login_user.password , db_user.password):  
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect username or password")
    
    acess_token = create_access_token({"sub":str(db_user.id), "token_type": "bearer"})

    return {"access_token":acess_token}

