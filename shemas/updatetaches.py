from pydantic import BaseModel,EmailStr,Field
from enum import Enum

class Priority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Update_ValideTaches(BaseModel):
    title:str = Field(min_lenght=2)
    description:str | None 
    priority:Priority 
