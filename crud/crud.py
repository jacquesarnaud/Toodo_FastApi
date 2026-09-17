from models.models import ModelTache
from database.database import Session


def get_tache(db:Session): 
    return db.query(ModelTache).all()