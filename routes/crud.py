from sqlalchemy.orm import Session
from routes import models

def get_ordens(db: Session):
    return db.query(models.OrdemDeServico).all()

def create_ordem(db: Session, descricao: str):
    ordem = models.OrdemDeServico(descricao=descricao)
    db.add(ordem)
    db.commit()
    db.refresh(ordem)
    return ordem
