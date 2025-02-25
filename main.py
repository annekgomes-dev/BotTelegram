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

# Função de início que exibe opções para o usuário
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    if chat_id not in usuarios_os:  # Evitar saudação duplicada
        bot.send_message(chat_id, "👋 Olá! Eu sou o OSBot, o Bot Online da FixTech. Vou te ajudar a registrar e acompanhar suas Ordens de Serviço (OS) de forma rápida e fácil.\n\n🔹 Para sair a qualquer momento, digite SAIR.\n\nComo posso te ajudar? Escolha uma opção abaixo:", reply_markup=menu_principal())

def menu_principal():
    markup = types.InlineKeyboardMarkup()
    criar_os_btn = types.InlineKeyboardButton("📌 Criar OS", callback_data="criar_os")
    ver_status_btn = types.InlineKeyboardButton("📊 Ver Status", callback_data="ver_status")
    base_conhecimento_btn = types.InlineKeyboardButton("📚 Base de Conhecimento", callback_data="base_conhecimento")
    markup.add(criar_os_btn, ver_status_btn, base_conhecimento_btn)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id

    if call.data == "criar_os":
        bot.send_message(chat_id, "🔹 **Por favor, informe seu login de rede:** (Exemplo: Nome.sobrenome)")
        bot.register_next_step_handler_by_chat_id(chat_id, obter_login)

    elif call.data == "ver_status":
        bot.send_message(chat_id, "🔹 **Me informe o número da sua OS:**")
        bot.register_next_step_handler_by_chat_id(chat_id, verificar_status_os)

    elif call.data == "base_conhecimento":
        bot.send_message(chat_id, "🔹 **Por favor, informe uma breve descrição do problema que você está enfrentando:**")
        bot.register_next_step_handler_by_chat_id(chat_id, buscar_base_conhecimento)

    elif call.data in ["fabrica_I", "fabrica_II"]:
        usuarios_os[chat_id]['unidade'] = "Fábrica I" if call.data == "fabrica_I" else "Fábrica II"
        bot.send_message(chat_id, "🔹 **Informe seu setor:**", reply_markup=setor_markup())

    elif call.data in ["incidente", "requisicao"]:
        usuarios_os[chat_id]['tipo'] = call.data
        bot.send_message(chat_id, "🔹 **Qual é a URGÊNCIA da sua OS?**", reply_markup=urgencia_markup())

    elif call.data in ["alta", "media", "baixa"]:
        usuarios_os[chat_id]['urgencia'] = call.data
        numero_os = usuarios_os[chat_id]['numero_os']
        bot.send_message(chat_id, f"✅ *Pronto!* Sua OS foi criada com sucesso!\n\n"
                                  f"**Resumo da OS:**\n"
                                  f"**Login:** {usuarios_os[chat_id]['login']}\n"
                                  f"**Unidade:** {usuarios_os[chat_id]['unidade']}\n"
                                  f"**Setor:** {usuarios_os[chat_id]['setor']}\n"
                                  f"**Título:** {usuarios_os[chat_id]['titulo']}\n"
                                  f"**Tipo:** {usuarios_os[chat_id]['tipo']}\n"
                                  f"**Urgência:** {usuarios_os[chat_id]['urgencia']}\n"
                                  f"**Linha:** {usuarios_os[chat_id].get('linha', 'N/A')}\n"
                                  f"**Área de Produção:** {usuarios_os[chat_id].get('area_producao', 'N/A')}\n"
                                  f"\n**Seu número da OS é:** {numero_os}\n"
                                  f"Para acompanhar, basta escolher a opção 2.")
    else:
        usuarios_os[chat_id]['setor'] = call.data
        bot.send_message(chat_id, "🔹 **Me informe um título para seu chamado:**")
        bot.register_next_step_handler_by_chat_id(chat_id, obter_titulo)

def obter_login(message):
    chat_id = message.chat.id
    login_usuario = message.text.strip()
    usuarios_os[chat_id] = {
        'login': login_usuario,
        'numero_os': random.randint(100000, 999999)
    }
    bot.send_message(chat_id, "🔹 **Me informe a unidade que você pertence:**", reply_markup=unidade_markup())

def unidade_markup():
    markup = types.InlineKeyboardMarkup()
    fab1_btn = types.InlineKeyboardButton("🏭 Fábrica I", callback_data="fabrica_I")
    fab2_btn = types.InlineKeyboardButton("🏭 Fábrica II", callback_data="fabrica_II")
    markup.add(fab1_btn, fab2_btn)
    return markup

def setor_markup():
    markup = types.InlineKeyboardMarkup()
    setores = ["Almoxarifado", "Área Técnica - Produção", "Área Técnica de Projetos",
               "Compras", "Contabilidade", "Controle da Qualidade", "Custos",
               "Diretoria", "Engenharia", "Expedição", "Faturamento",
               "Financeiro", "Fiscal", "Jurídico", "Planej. e Controle da Produção",
               "Produção", "Recepção", "Recursos Humanos", "SESMT", "SGI", "SMD",
               "Tecnologia da Informação"]
    for setor in setores:
        markup.add(types.InlineKeyboardButton(setor, callback_data=setor))
    return markup

def obter_titulo(message):
    chat_id = message.chat.id
    titulo_os = message.text.strip()
    usuarios_os[chat_id]['titulo'] = titulo_os
    bot.send_message(chat_id, "🔹 **Seu chamado é um:**", reply_markup=tipo_os_markup())

def tipo_os_markup():
    markup = types.InlineKeyboardMarkup()
    incidente_btn = types.InlineKeyboardButton("🚨 Incidente (Sinistro/problema)", callback_data="incidente")
    requisicao_btn = types.InlineKeyboardButton("📝 Requisição (Solicitação)", callback_data="requisicao")
    markup.add(incidente_btn, requisicao_btn)
    return markup

def urgencia_markup():
    markup = types.InlineKeyboardMarkup()
    alta_btn = types.InlineKeyboardButton("⚠️ Alta", callback_data="alta")
    media_btn = types.InlineKeyboardButton("⚠️ Média", callback_data="media")
    baixa_btn = types.InlineKeyboardButton("⬇️ Baixa", callback_data="baixa")
    markup.add(alta_btn, media_btn, baixa_btn)
    return markup

def verificar_status_os(message):
    chat_id = message.chat.id
    numero_os = message.text.strip()
    if numero_os in [str(usuario['numero_os']) for usuario in usuarios_os.values()]:
        for usuario in usuarios_os.values():
            if usuario['numero_os'] == int(numero_os):
                status = "Em andamento"
                bot.send_message(chat_id, f"🔍 OS encontrada com sucesso!\n\n"
                                          f"**ID:** {usuario['numero_os']}\n"
                                          f"**Data de Abertura:** [Data aqui]\n"
                                          f"**Título:** {usuario['titulo']}\n"
                                          f"**Status:** {status}")
                return
    bot.send_message(chat_id, "⚠️ OS não encontrada. Verifique o número e tente novamente.")

def buscar_base_conhecimento(message):
    chat_id = message.chat.id
    descricao = message.text.strip()
    bot.send_message(chat_id, f"🔎 **Buscando soluções para:** {descricao}...\n*Esta funcionalidade ainda está em desenvolvimento!*")

@bot.message_handler(func=lambda message: message.text.lower() == "sair")
def sair_conversa(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "👋 Você saiu da conversa. Até mais!")

if __name__ == "__main__":
    bot.polling()
