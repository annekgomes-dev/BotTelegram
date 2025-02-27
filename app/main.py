import os
import random
import datetime
import requests
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN_TELEGRAM')
GLPI_API_URL = os.getenv("GLPI_API_URL")
GLPI_APP_TOKEN = "SEU_APP_TOKEN"  # Substitua pelo token da sua aplicação
GLPI_USER_TOKEN = "SEU_USER_TOKEN"  # Substitua pelo token do usuário

bot = telebot.TeleBot(TOKEN)
usuarios_os = {}

def obter_saudacao():
    hora = datetime.datetime.now().hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def get_glpi_session():
    headers = {
        "App-Token": GLPI_APP_TOKEN,
        "Authorization": f"user_token {GLPI_USER_TOKEN}",
    }
    response = requests.get(f"{GLPI_API_URL}/initSession", headers=headers)
    if response.status_code == 200:
        return response.json().get("session_token")
    else:
        print(f"Erro ao iniciar sessão: {response.text}")
        return None

def start_message(message):
    chat_id = message.chat.id
    nome_usuario = message.from_user.first_name
    saudacao = obter_saudacao()
    bot.send_message(chat_id, f"{saudacao}, {nome_usuario}! Eu sou o OSBot.", reply_markup=menu_principal())

def menu_principal():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📌 Criar OS", callback_data="criar_os"))
    markup.add(types.InlineKeyboardButton("🔎 Status OS", callback_data="ver_status"))
    markup.add(types.InlineKeyboardButton("📚 Base de Conhecimento", callback_data="base_conhecimento"))
    return markup

def obter_login(message):
    chat_id = message.chat.id
    login_usuario = message.text.strip()
    usuarios_os[chat_id] = {
        'login': login_usuario,
        'numero_os': random.randint(1, 3000)
    }
    bot.send_message(chat_id, "Informe a unidade:", reply_markup=unidade_markup())

def unidade_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏭 Fábrica I", callback_data="fabrica_I"))
    markup.add(types.InlineKeyboardButton("🏭 Fábrica II", callback_data="fabrica_II"))
    return markup

def callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "criar_os":
        bot.send_message(chat_id, "Informe seu login de rede:")
        bot.register_next_step_handler_by_chat_id(chat_id, obter_login)
    elif call.data == "ver_status":
        bot.send_message(chat_id, "Me informe o número da sua OS:")
        bot.register_next_step_handler_by_chat_id(chat_id, verificar_status_os)

def verificar_status_os(message):
    chat_id = message.chat.id
    numero_os = message.text.strip()
    encontrado = False
    for usuario in usuarios_os.values():
        if usuario['numero_os'] == int(numero_os):
            bot.send_message(chat_id, f"OS encontrada! ID: {usuario['numero_os']} - Status: Em andamento")
            encontrado = True
            break
    if not encontrado:
        bot.send_message(chat_id, "OS não encontrada. Verifique o número e tente novamente.")

if __name__ == "__main__":
    session_token = get_glpi_session()
    if session_token:
        print("GLPI Session iniciada com sucesso")
    print("Rodando")
    bot.polling(timeout=60)
