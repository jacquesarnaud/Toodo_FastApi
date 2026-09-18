from database.database import Base
from sqlalchemy import Column,String,Boolean,Integer,DateTime,ForeignKey,Enum as QSLENUM
from datetime import datetime
from enum import Enum

class ModelUser(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name =Column(String)
    email =Column(String)
    password =Column(String)
    createdAt = Column(DateTime, default=datetime.now)


class Priority(str,Enum):
    low = "low"
    medium = "medium"
    high = "high"

class ModelTache(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String,QSLENUM(Priority))
    completed = Column(Boolean , default=False)
    # userId = Column(Integer, ForeignKey("ModelUser.id"))
    createdAt = Column(DateTime, default=datetime.date)