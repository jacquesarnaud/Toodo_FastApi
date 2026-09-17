from sqlalchemy import create_engine
from fastapi import Depends
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from typing import Annotated

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

sessionlocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base =declarative_base()

def get_bd():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_bd)]




