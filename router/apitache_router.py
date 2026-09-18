from fastapi import APIRouter,Path,HTTPException,Body
from starlette import status
from database.database import db_dependency
from models.models import ModelTache
from typing import Annotated
from shemas.PostTaches import Post_ValideTaches


router_tache = APIRouter(prefix="/tache" , tags=["Tache"])


@router_tache.get("", status_code=status.HTTP_200_OK)
async def get_all_taches (db:db_dependency):
    taches = db.query(ModelTache).all()
    return taches


@router_tache.get("/{id_tasks}", status_code=status.HTTP_200_OK)
async def get_taches_by_id (db:db_dependency,id_tasks:Annotated[int,Path(ge=0,title="recupéré l'ID de la tache")]):
    taches = db.query(ModelTache).filter(ModelTache.id == id_tasks ).first()
    if taches:
        return taches
    raise HTTPException(status_code=404, detail="tasks not found")



@router_tache.post("/create",status_code=status.HTTP_201_CREATED)
async def create_tache(db:db_dependency,tasks:Annotated[Post_ValideTaches,Body(title="creattion de tache",example={
    "title": "mon titre",
    "priority": "high",
    "completed": False,
    "id": 1,
    "description": "un titre tres simple mais qui parle",
    "createdAt": "2026-09-18T15:36:05.287737"
  })]):
    new_tache = ModelTache(title=tasks.title,description=tasks.description,priority=tasks.priority)
    db.add(new_tache)
    db.commit()
    db.refresh(new_tache)
    return(new_tache)