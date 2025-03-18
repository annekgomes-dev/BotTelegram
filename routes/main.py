from fastapi import FastAPI
import os, users, bot, os as os_routes

app = FastAPI()

app.include_router(os_routes.router, prefix="/os", tags=["Ordens de Serviço"])
app.include_router(users.router, prefix="/users", tags=["Usuários"])
app.include_router(bot.router, prefix="/bot", tags=["Bot Telegram"])

@app.get("/")
def read_root():
    return {"message": "OSBot API is running"}
