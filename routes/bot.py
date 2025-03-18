import os
import random
import datetime
import telebot
from telebot import types
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN_TELEGRAM')
API_URL = "http://127.0.0.1:8000"  # URL da API FastAPI

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


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    nome_usuario = message.from_user.first_name
    saudacao = obter_saudacao()
    bot.send_message(chat_id, f"{saudacao}, {nome_usuario}! Eu sou o OSBot.", reply_markup=menu_principal())


def menu_principal():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📌 Criar OS", callback_data="criar_os"))
    markup.add(types.InlineKeyboardButton("🔎 Status OS", callback_data="ver_status"))
    return markup


@bot.callback_query_handler(func=lambda call: call.data in ["criar_os", "ver_status"])
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "criar_os":
        bot.send_message(chat_id, "Informe seu login de rede:")
        bot.register_next_step_handler_by_chat_id(chat_id, verificar_usuario)
    elif call.data == "ver_status":
        bot.send_message(chat_id, "Me informe o número da sua OS:")
        bot.register_next_step_handler_by_chat_id(chat_id, verificar_status_os)


def verificar_usuario(message):
    chat_id = message.chat.id
    login_usuario = message.text.strip()

    # Consulta o usuário no banco de dados via API
    response = requests.get(f"{API_URL}/users/{login_usuario}")

    if response.status_code == 200:
        usuario = response.json()
        usuarios_os[chat_id] = {"login": usuario["login"], "nome": usuario["nome"]}
        bot.send_message(chat_id, "Usuário encontrado! Descreva o problema:")
        bot.register_next_step_handler_by_chat_id(chat_id, registrar_os)
    else:
        bot.send_message(chat_id, "Usuário não encontrado. Verifique seu login e tente novamente.")


def registrar_os(message):
    chat_id = message.chat.id
    descricao = message.text.strip()
    usuario = usuarios_os.get(chat_id)

    if usuario:
        numero_os = random.randint(1000, 9999)
        payload = {
            "numero_os": numero_os,
            "login": usuario["login"],
            "titulo": "OS Criada via Telegram",
            "descricao": descricao,
            "tipo_os": "Incidente",  # Padrão para teste
            "urgencia": "Média",  # Padrão para teste
        }
        response = requests.post(f"{API_URL}/ordem_servico/", json=payload)

        if response.status_code == 201:
            bot.send_message(chat_id, f"OS criada com sucesso! Número: {numero_os}")
        else:
            bot.send_message(chat_id, "Erro ao criar OS. Tente novamente mais tarde.")
    else:
        bot.send_message(chat_id, "Erro ao registrar OS. Comece novamente com /start.")


def verificar_status_os(message):
    chat_id = message.chat.id
    numero_os = message.text.strip()

    response = requests.get(f"{API_URL}/ordem_servico/{numero_os}")

    if response.status_code == 200:
        os_data = response.json()
        bot.send_message(chat_id, f"OS {os_data['numero_os']} - Status: {os_data['status']}")
    else:
        bot.send_message(chat_id, "OS não encontrada. Verifique o número e tente novamente.")


if __name__ == "__main__":
    print("OSBot rodando...")
    bot.polling(timeout=60)
