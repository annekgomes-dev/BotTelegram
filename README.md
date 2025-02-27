# OSBot - Bot de Ordens de Serviço integrado ao GLPI

## Descrição
O **OSBot** é um chatbot desenvolvido para o Telegram, projetado para facilitar a criação e o gerenciamento de Ordens de Serviço (OS) dentro de uma fábrica. Ele se integra ao **GLPI**, um sistema de gerenciamento de ativos e suporte técnico, permitindo aos usuários criar, acompanhar e consultar a base de conhecimento diretamente pelo Telegram.

---

## 🛠 Tecnologias Utilizadas
- **Python** (com a biblioteca `pyTelegramBotAPI` para o bot do Telegram)
- **Docker & Docker Compose** (para containerização dos serviços)
- **PostgreSQL** (banco de dados para o GLPI)
- **GLPI** (sistema de gerenciamento de TI)

---

## 🚀 Como Configurar e Rodar o Projeto

### 1️⃣ Clonar o repositório
```sh
git clone https://github.com/seu-usuario/osbot-glpi.git
cd osbot-glpi
```

### 2️⃣ Criar o arquivo `.env`
Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
```env
TOKEN_TELEGRAM=SEU_TOKEN_AQUI
GLPI_API_URL=http://meu_glpi/front/api.php
GLPI_APP_TOKEN=SEU_APP_TOKEN
GLPI_USER_TOKEN=SEU_USER_TOKEN
```
- **`TOKEN_TELEGRAM`**: Obtenha criando um bot no Telegram via `@BotFather`.
- **`GLPI_API_URL`**: Normalmente `http://meu_glpi/front/api.php` se rodando em Docker.
- **`GLPI_APP_TOKEN`**: Gere no GLPI em **Configuração → API**.
- **`GLPI_USER_TOKEN`**: Gere no GLPI em **Preferências → Tokens API**.

### 3️⃣ Rodar os Containers com Docker Compose
```sh
docker-compose up -d --build
```
Esse comando irá subir os seguintes containers:
- **PostgreSQL** (banco de dados)
- **GLPI** (sistema de gestão de TI)
- **OSBot** (bot Telegram rodando em Python)

### 4️⃣ Verificar os Logs
Para ver se o bot está rodando corretamente, execute:
```sh
docker logs -f meu_bot
```

### 5️⃣ Testar o Bot no Telegram
- Envie `/start` para o bot no Telegram e siga as instruções interativas.
- Teste a criação e consulta de OS.

---

## 📌 Endpoints da API GLPI Utilizados
O bot se comunica com o GLPI usando sua API REST. Alguns endpoints importantes:
- **Autenticação** (`/initSession`)
- **Criar Ordem de Serviço** (`/Ticket`)
- **Buscar Ordem de Serviço** (`/Ticket/:id`)

---

## ❌ Como Parar os Containers
```sh
docker-compose down
```
Isso irá desligar todos os containers do projeto.

---

## 📖 Melhorias Futuras
- Implementar melhor consulta à Base de Conhecimento do GLPI.
- Melhorar a interface do bot com mais opções interativas.
- Adicionar logs estruturados para facilitar a monitoração.

---

## 📝 Licença
Este projeto é open-source e pode ser usado e modificado conforme a necessidade.

---

Se tiver qualquer dúvida ou sugestão, fique à vontade para contribuir! 🚀