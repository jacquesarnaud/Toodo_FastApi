from fastapi import APIRouter
from starlette import status
from database.database import db_dependency
from crud.crud import get_tache
from models.models import ModelTache

router_tache = APIRouter(prefix="/tache" , tags=["Tache"])


@router_tache.get("", status_code=status.HTTP_200_OK)
async def get_all_taches (db:db_dependency):
    taches = get_tache(db=db_dependency)
    return taches



