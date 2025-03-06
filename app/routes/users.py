from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import criar_usuario
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuarios/")
def criar_usuario_endpoint(nome: str, email: str, db: Session = Depends(get_db)):
    return criar_usuario(db, nome, email)
