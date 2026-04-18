import json
import os
import uuid
from datetime import datetime
from threading import Lock

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'tasks.json')
file_lock = Lock()

def _load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_data(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def get_all_tasks():
    with file_lock:
        return _load_data()

def add_task(title, description, task_date, task_time):
    with file_lock:
        tasks = _load_data()
        new_task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "date": task_date, # YYYY-MM-DD
            "time": task_time, # HH:MM
            "completed": False,
            "notified_milestones": [], # Lista de marcos já avisados: ["7d", "24h", "5h", "1h", "10m"]
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tasks.append(new_task)
        _save_data(tasks)
        return new_task

def complete_task(task_id):
    with file_lock:
        tasks = _load_data()
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = True
                _save_data(tasks)
                return True
    return False

def delete_task(task_id):
    with file_lock:
        tasks = _load_data()
        original_len = len(tasks)
        tasks = [t for t in tasks if t['id'] != task_id]
        if len(tasks) < original_len:
            _save_data(tasks)
            return True
    return False

def mark_milestone_notified(task_id, milestone):
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
