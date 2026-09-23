from fastapi import APIRouter,Path,HTTPException,Body,Depends,Query
from starlette import status
from database.database import db_dependency
from models.models import ModelTache,ModelUser
from typing import Annotated

from Auth.dependece import curent_dependancy
from shemas.PostTaches import Post_ValideTaches , Priority,Taches
from shemas.updatetaches import Update_ValideTaches

from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router_tache = APIRouter(prefix="/tache" , tags=["Tache"])


@router_tache.get("", status_code=status.HTTP_200_OK)
async def get_all_taches (curent_user:curent_dependancy,db:db_dependency)->Page[Taches]:

    return paginate(db, select(ModelTache).order_by(ModelTache.createdAt).filter(ModelTache.userId == curent_user.id))
        
# @router_tache.get("/text")
# def get_users(db:db_dependency)->Page[Taches]:
#     return paginate(db, select(ModelTache).order_by(ModelTache.createdAt))

@router_tache.get("/{id_tasks}", status_code=status.HTTP_200_OK)
async def get_taches_by_id (curent_user:curent_dependancy,db:db_dependency,id_tasks:Annotated[int,Path(ge=0,title="recupéré l'ID de la tache")]):
    taches = db.query(ModelTache).filter(ModelTache.id == id_tasks and ModelTache.id == curent_user.id ).first()
    if not taches:
        raise HTTPException(status_code=404, detail="tasks not found")
    return taches


@router_tache.get("/filtre" , status_code=status.HTTP_200_OK)
async def seach(curent_user:curent_dependancy,db:db_dependency, priority:Annotated[Priority|None,Query()]= None ,completed:Annotated[bool|None,Query()]=None):
    if priority:
        return db.query(ModelTache).filter(ModelTache.priority == priority and ModelTache.userId == curent_user).all()
    if completed:
        return db.query(ModelTache).filter(ModelTache.completed == completed and ModelTache.userId == curent_user).all()


@router_tache.post("/create",status_code=status.HTTP_201_CREATED)
async def create_tache(curent_user:curent_dependancy,db:db_dependency,tasks:Annotated[Post_ValideTaches,Body(title="creattion de tache",example={
    "title": "mon titre",
    "priority": "high",
    "completed": False,
    "id": 1,
    "description": "un titre tres simple mais qui parle",
    "createdAt": "2026-09-18T15:36:05.287737"
  })]):
    new_tache = ModelTache(title=tasks.title,description=tasks.description,priority=tasks.priority,userId=curent_user.id)
    db.add(new_tache)
    db.commit()
    db.refresh(new_tache)
    return(new_tache)

@router_tache.put("/update/tasks/{id_tasks}",status_code=status.HTTP_200_OK)
async def update_tache(db:db_dependency,id_tasks:Annotated[int,Path(ge=0)],curent_user:curent_dependancy,body_tache:Annotated[Update_ValideTaches,Body()]):
    tache_exit= db.query(ModelTache).filter(ModelTache.id == id_tasks and ModelTache.userId==curent_user.id).first()
    if not tache_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="tache introuvé")
    tache_exit.title=body_tache.title
    tache_exit.description=body_tache.description
    tache_exit.priority=body_tache.priority
    db.add(tache_exit)
    db.commit()
    db.refresh(tache_exit)
    return tache_exit

@router_tache.patch("/patch/tasks/{id_tasks}/complete",status_code=status.HTTP_200_OK)
async def patch_tache(db:db_dependency,id_tasks:Annotated[int,Path(ge=0)],curent_user:curent_dependancy,):
    tache_exit= db.query(ModelTache).filter(ModelTache.id == id_tasks and ModelTache.userId==curent_user.id).first()
    if not tache_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="tache introuvé")
    tache_exit.completed = True
    db.add(tache_exit)
    db.commit()
    db.refresh(tache_exit)
    return tache_exit

@router_tache.delete("/delete/tasks/{id_tasks}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_tache(db:db_dependency,id_tasks:Annotated[int,Path(ge=0)],curent_user:curent_dependancy):
    tache_exit= db.query(ModelTache).filter(ModelTache.id == id_tasks and ModelTache.userId==curent_user.id).first()
    if not tache_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="tache introuvé")
    db.delete(tache_exit)
    db.commit()
    