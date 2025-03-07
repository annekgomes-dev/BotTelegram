from fastapi import FastAPI
from app.routes import users, os
from app.routes.database import engine, Base

app = FastAPI()

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Incluir as rotas
app.include_router(users.router, prefix="/api")
app.include_router(os.router, prefix="/api")
