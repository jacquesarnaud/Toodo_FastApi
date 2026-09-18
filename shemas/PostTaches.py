from pydantic import BaseModel,Field
from enum import Enum
from datetime import datetime


class Priority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Post_ValideTaches(BaseModel):
    title:str = Field(min_lenght=2)
    description:str | None 
    priority:Priority 
    completed:bool = Field(default=False)
    createdAt :str =Field(default=datetime.now()) 

    model_config={
        "json_schema_extra":{
            "examples":[
                {
                    "id":0,
                    "title":"mon titre",
                    "description": "un titre tres simple mais qui parle",
                    "priority":"high",
                    "completed":False,
                }
            ]
        }
    }