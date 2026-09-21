from pydantic import BaseModel,fields,EmailStr

class User_create (BaseModel):
    name : str = None
    email : EmailStr 
    password:str 