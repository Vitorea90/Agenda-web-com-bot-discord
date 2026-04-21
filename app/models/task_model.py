import json
import os
import uuid
import logging
from datetime import datetime
from threading import Lock
from typing import List, Dict, Optional, Any

# Configuração do logger para o modelo
logger = logging.getLogger(__name__)

# Caminho para o arquivo de dados
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'tasks.json')
file_lock = Lock()

def _load_data() -> List[Dict[str, Any]]:
    """
    Carrega as tarefas do arquivo JSON de forma segura.
    Retorna uma lista vazia se o arquivo não existir ou estiver corrompido.
    """
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Erro ao ler arquivo de dados: {e}")
        return []

def _save_data(tasks: List[Dict[str, Any]]) -> bool:
    """
    Salva a lista de tarefas no arquivo JSON.
    Retorna True se salvou com sucesso, False caso contrário.
    """
    try:
        # Garante que o diretório exista
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        logger.error(f"Erro ao salvar arquivo de dados: {e}")
        return False

def get_all_tasks() -> List[Dict[str, Any]]:
    """
    Retorna todas as tarefas cadastradas sob proteção de lock.
    """
    with file_lock:
        return _load_data()

def add_task(title: str, description: Optional[str], task_date: str, task_time: str) -> Dict[str, Any]:
    """
    Cria e persiste uma nova tarefa.
    :param title: Título da tarefa
    :param description: Detalhes adicionais (opcional)
    :param task_date: Data no formato YYYY-MM-DD
    :param task_time: Hora no formato HH:MM
    """
    with file_lock:
        tasks = _load_data()
        new_task = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "description": description.strip() if description else "",
            "date": task_date,
            "time": task_time,
            "completed": False,
            "notified_milestones": [], # Marcos (10m, 1h, etc) para evitar duplicidade no bot
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tasks.append(new_task)
        _save_data(tasks)
        logger.info(f"Nova tarefa adicionada: {new_task['title']} (ID: {new_task['id']})")
        return new_task

def complete_task(task_id: str) -> bool:
    """
    Marca uma tarefa como concluída pelo seu ID.
    """
    with file_lock:
        tasks = _load_data()
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = True
                _save_data(tasks)
                logger.info(f"Tarefa marcada como concluída: ID {task_id}")
                return True
    return False

def delete_task(task_id: str) -> bool:
    """
    Remove permanentemente uma tarefa da base de dados.
    """
    with file_lock:
        tasks = _load_data()
        nova_lista = [t for t in tasks if t['id'] != task_id]
        if len(nova_lista) < len(tasks):
            _save_data(nova_lista)
            logger.info(f"Tarefa removida: ID {task_id}")
            return True
    return False

def mark_milestone_notified(task_id: str, milestone: str) -> bool:
    """
    Registra que uma notificação específica já foi enviada pelo Bot.
    """
    with file_lock:
        tasks = _load_data()
        for task in tasks:
            if task['id'] == task_id:
                if "notified_milestones" not in task:
                    task['notified_milestones'] = []
                if milestone not in task['notified_milestones']:
                    task['notified_milestones'].append(milestone)
                    _save_data(tasks)
                    return True
    return False

