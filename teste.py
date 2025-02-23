import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")

# Verificação do Token
if not TOKEN_TELEGRAM:
    raise ValueError("Erro: TOKEN_TELEGRAM não foi encontrado no .env")
else:
    print(f"✅ Token carregado com sucesso: {TOKEN_TELEGRAM[:10]}********")