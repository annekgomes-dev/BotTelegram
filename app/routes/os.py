from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Usuario, OrdemServico
from app.crud import criar_usuario, criar_ordem_servico

router = APIRouter()
