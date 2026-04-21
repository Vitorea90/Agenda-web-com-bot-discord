# 📅 Agenda Web + Bot Discord (MVC)

Este projeto é um sistema de gerenciamento de tarefas que integra uma interface web Flask com notificações automáticas via Discord. A aplicação foi estruturada seguindo o padrão **MVC (Model-View-Controller)** para garantir modularidade e facilidade de manutenção.

## 🛠️ Tecnologias e Arquitetura

- **Backend**: Python 3.10+ (Flask como servidor web).
- **Notificações**: Discord.py (Bot assíncrono).
- **Banco de Dados**: Persistência em arquivos JSON com proteção de `threading.Lock`.
- **Frontend**: HTML5, CSS3 e Bootstrap 5 para um design responsivo.
- **Logs**: Sistema de logging centralizado salvando em `app.log`.

## 📁 Estrutura do Repositório

```text
agenda_discord/
├── app/
│   ├── controllers/    # Processamento de rotas e lógica de negócio
│   ├── models/         # Manipulação de dados e persistência
│   ├── static/         # Arquivos estáticos (CSS/JS)
│   ├── templates/      # Estruturas HTML (Jinja2)
├── bot/                # Lógica de integração e loop do Discord
├── data/               # Armazenamento físico (tasks.json)
├── run.py              # Ponto de entrada (Flask em Thread + Bot)
├── requirements.txt    # Dependências com versões fixas
└── README.md           # Documentação técnica
```

## 🚀 Instalação e Execução

### 1. Preparação do Ambiente
Recomenda-se o uso de um ambiente virtual:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Instalação de Dependências
```bash
pip install -r requirements.txt
```

### 3. Configuração de Variáveis (`.env`)
Renomeie o arquivo `.env.example` para `.env` e preencha as credenciais do seu Bot do Discord:
- `DISCORD_TOKEN`: Token gerado no Discord Developer Portal.
- `DISCORD_CHANNEL_ID`: ID do canal de texto para notificações globais.
- `DISCORD_USER_ID`: (Opcional) Seu ID de usuário para notificações via DM.

### 4. Executando o Sistema
```bash
python run.py
```
O servidor web iniciará em `http://localhost:5000` e o bot se conectará simultaneamente.

## 📋 Funcionalidades Técnicas
- **CRUD Completo**: Adição, conclusão e remoção de tarefas via web.
- **Check Inteligente**: O bot verifica tarefas no arquivo JSON a cada 60 segundos.
- **Múltiplos Avisos**: Notificações configuráveis (7 dias, 24h, 5h, 1h e 10 min antes).
- **Logs de Auditoria**: Atividades do sistema e erros são registrados tanto no console quanto em arquivo.

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

