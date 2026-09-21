from pydantic import BaseModel,EmailStr


class User_log(BaseModel):
    email : EmailStr
    password : str