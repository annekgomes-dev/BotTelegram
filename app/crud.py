from sqlalchemy.orm import Session
from app.models import Usuario, OrdemServico

def criar_usuario(db: Session, nome: str, email: str):
    usuario = Usuario(nome=nome, email=email)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def criar_ordem_servico(db: Session, descricao: str, usuario_id: int):
    ordem = OrdemServico(descricao=descricao, usuario_id=usuario_id)
    db.add(ordem)
    db.commit()
    db.refresh(ordem)
    return ordem
