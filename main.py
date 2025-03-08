import telebot
from telebot import types
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN_TELEGRAM')
bot = telebot.TeleBot(TOKEN)

# Dicionário para armazenar dados das Ordens de Serviço
usuarios_os = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     "\U0001F44B Olá! Eu sou o OSBot, o Bot Online da FixTech. Vou te ajudar a registrar e acompanhar suas Ordens de Serviço (OS) de forma rápida e fácil.\n\n\U0001F449 Para sair a qualquer momento, digite SAIR.\n\nComo posso te ajudar? Escolha uma opção abaixo:",
                     reply_markup=menu_principal())


@bot.message_handler(func=lambda message: True)
def qualquer_mensagem(message):
    start_message(message)


def menu_principal():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📌 Criar OS", callback_data="criar_os"))
    markup.add(types.InlineKeyboardButton("🔎 Status OS", callback_data="ver_status"))
    markup.add(types.InlineKeyboardButton("📚 Base de Conhecimento", callback_data="base_conhecimento"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id

    if call.data == "criar_os":
        bot.send_message(chat_id, "🔹 **Por favor, informe seu login de rede:** (Exemplo: nome.sobrenome)")
        bot.register_next_step_handler_by_chat_id(chat_id, obter_login)
    elif call.data == "ver_status":
        bot.send_message(chat_id, "🔹 **Me informe o número da sua OS:**")
        bot.register_next_step_handler_by_chat_id(chat_id, verificar_status_os)
    elif call.data == "base_conhecimento":
        bot.send_message(chat_id, "🔹 **Descreva brevemente o problema que você está enfrentando:**")
        bot.register_next_step_handler_by_chat_id(chat_id, buscar_base_conhecimento)


def obter_login(message):
    chat_id = message.chat.id
    login_usuario = message.text.strip()
    usuarios_os[chat_id] = {
        'login': login_usuario,
        'numero_os': random.randint(1, 3000)
    }
    bot.send_message(chat_id, "🔹 **Me informe a unidade que você pertence:**", reply_markup=unidade_markup())


def verificar_status_os(message):
    chat_id = message.chat.id
    numero_os = message.text.strip()
    if numero_os in [str(usuario['numero_os']) for usuario in usuarios_os.values()]:
        for usuario in usuarios_os.values():
            if usuario['numero_os'] == int(numero_os):
                status = "Em andamento"
                bot.send_message(chat_id,
                                 f"🔍 **OS encontrada com sucesso!**\n\n**ID:** {usuario['numero_os']}\n**Título:** {usuario.get('titulo', 'N/A')}\n**Status:** {status}")
                return
    bot.send_message(chat_id, "⚠️ **OS não encontrada. Verifique o número e tente novamente.**")


def buscar_base_conhecimento(message):
    chat_id = message.chat.id
    descricao = message.text.strip()
    bot.send_message(chat_id,
                     f"🔎 **Buscando soluções para:** {descricao}...\n**Esta funcionalidade ainda está em desenvolvimento!**")


def unidade_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏭 Fábrica I", callback_data="fabrica_I"))
    markup.add(types.InlineKeyboardButton("🏭 Fábrica II", callback_data="fabrica_II"))
    return markup


def setor_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Produção", callback_data="producao"))
    markup.add(types.InlineKeyboardButton("Manutenção", callback_data="manutencao"))
    markup.add(types.InlineKeyboardButton("TI", callback_data="ti"))
    markup.add(types.InlineKeyboardButton("RH", callback_data="rh"))
    return markup


def urgencia_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔥 Alta", callback_data="alta"))
    markup.add(types.InlineKeyboardButton("⚠️ Média", callback_data="media"))
    markup.add(types.InlineKeyboardButton("✅ Baixa", callback_data="baixa"))
    return markup


def obter_titulo(message):
    chat_id = message.chat.id
    usuarios_os[chat_id]['titulo'] = message.text.strip()
    bot.send_message(chat_id, "🔹 **Selecione o tipo de OS:**", reply_markup=tipo_os_markup())


def tipo_os_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚨 Incidente", callback_data="incidente"))
    markup.add(types.InlineKeyboardButton("🛠 Requisição", callback_data="requisicao"))
    return markup


@bot.message_handler(func=lambda message: message.text.lower() == "sair")
def sair_conversa(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "👋 Você saiu da conversa. Até mais!")


if __name__ == "__main__":
    print("Rodando")
    bot.polling(timeout=60)