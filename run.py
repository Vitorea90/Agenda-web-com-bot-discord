import threading
from app import create_app
from bot.discord_bot import run_bot
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

app = create_app()

def start_flask():
    """Inicia o servidor Flask."""
    # Usando debug=False em threads para evitar recursão do reloader
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # 1. Inicia o Flask em uma thread separada
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("Servidor Flask iniciado em http://localhost:5000")
    
    # 2. Inicia o Bot do Discord (bloqueante na main thread)
    print("Iniciando Bot do Discord...")
    run_bot()
