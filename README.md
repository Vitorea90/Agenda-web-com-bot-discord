# 📅 Agenda Web Pro + Bot Discord

Um sistema de agenda completo e responsivo desenvolvido em Python, utilizando **Flask** para a interface web e **discord.py** para notificações automáticas em tempo real.

O projeto segue a arquitetura **MVC (Model-View-Controller)** para manter o código limpo, organizado e "humano".

## 🚀 Funcionalidades

- **Interface Web Premium**: Layout responsivo com Bootstrap 5, animações e design moderno.
- **Gestão de Tarefas**: CRUD completo (Adicionar, Listar, Concluir e Remover).
- **Notificações Inteligentes**: O Bot do Discord verifica as tarefas e envia um lembrete automático **5 minutos antes** do horário previsto.
- **Comandos no Discord**: Use `!tarefas` no seu servidor para ver o que está pendente diretamente pelo chat.
- **Persistência em JSON**: Dados salvos localmente de forma segura.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.10+
- **Framework Web**: Flask
- **Integração Discord**: discord.py
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5 & Bootstrap Icons)
- **Configuração**: python-dotenv

## 📦 Como Instalar

1.  **Clone o repositório** ou baixe os arquivos.
2.  **Crie um ambiente virtual** (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuração do Discord

Para que as notificações funcionem, você precisa de um Bot no Discord:

1.  Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2.  Crie uma nova aplicação e, na aba **Bot**, gere um **Token**.
3.  Ative a opção **Message Content Intent** nas configurações do Bot.
4.  Convide o Bot para o seu servidor com permissões de enviar mensagens e embeds.
5.  Copie o **ID do canal** onde deseja receber as notificações (clique com o botão direito no canal -> Copiar ID).
6.  Renomeie o arquivo `.env.example` para `.env` e preencha com suas credenciais:
    ```env
    DISCORD_TOKEN=seu_token_aqui
    DISCORD_CHANNEL_ID=seu_id_do_canal
    ```

## ▶️ Como Executar

Simplesmente execute o arquivo principal:

```bash
python run.py
```

- A interface web estará disponível em: `http://localhost:5000`
- O Bot do Discord iniciará simultaneamente no seu servidor.

## 📁 Estrutura do Projeto (MVC)

```text
agenda_discord/
├── app/
│   ├── controllers/    # Lógica de rotas (Flask)
│   ├── models/         # Manipulação de dados (JSON)
│   ├── static/         # CSS e assets visuais
│   ├── templates/      # Views HTML (Jinja2)
│   └── __init__.py     # Inicialização do App
├── bot/                # Lógica do Bot do Discord
├── data/               # Armazenamento (tasks.json)
├── run.py              # Arquivo de entrada principal
├── requirements.txt    # Dependências
└── README.md           # Documentação
```
