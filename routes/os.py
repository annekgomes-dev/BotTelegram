from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.database import get_db
from app.routes import crud

router = APIRouter()

@router.get("/")
def listar_ordens(db: Session = Depends(get_db)):
    return crud.get_ordens(db)

@router.post("/")
def criar_ordem(descricao: str, db: Session = Depends(get_db)):
    return crud.create_ordem(db, descricao)
