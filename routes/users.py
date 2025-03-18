from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from routes.models import Usuario

router = APIRouter()

@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()