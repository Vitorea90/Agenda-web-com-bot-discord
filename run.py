import threading
import logging
import os
from dotenv import load_dotenv
from app import create_app
from bot.discord_bot import run_bot

# Configuração de logging profissional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = create_app()

def start_flask():
    """ Inicia o servidor web Flask em modo de produção. """
    logger.info("Iniciando servidor web na porta 5000...")
    # Usando debug=False e use_reloader=False para rodar em thread
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    try:
        # 1. Inicia o Flask em uma thread separada (Daemon para encerrar com o processo pai)
        flask_thread = threading.Thread(target=start_flask, name="FlaskThread")
        flask_thread.daemon = True
        flask_thread.start()

        logger.info("Sistema de Agenda Web carregado com sucesso.")
        
        # 2. Inicia o Bot do Discord na thread principal (bloqueante)
        logger.info("Conectando ao Bot do Discord...")
        run_bot()
        
    except KeyboardInterrupt:
        logger.info("Encerrando sistema...")
    except Exception as e:
        logger.error(f"Erro fatal ao iniciar o sistema: {e}")

