from sqlalchemy import Column, Integer, String, Boolean
from app.routes.database import Base


class OrdemDeServico(Base):
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    status = Column(String, default="Aberto")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telegram_id = Column(String, unique=True, nullable=False)
