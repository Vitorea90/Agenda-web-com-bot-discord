import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import task_model

# Logger para o controlador
logger = logging.getLogger(__name__)

agenda_bp = Blueprint('agenda', __name__)

@agenda_bp.route('/')
def index():
    """ Página principal que lista todas as tarefas ordenadas por data/hora. """
    try:
        tasks = task_model.get_all_tasks()
        # Ordenação estável: tarefas concluídas por último, as pendentes por data
        tasks.sort(key=lambda t: (t['completed'], t['date'], t['time']))
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        logger.error(f"Erro ao carregar índice: {e}")
        flash("Ocorreu um erro ao carregar suas tarefas.", "error")
        return render_template('index.html', tasks=[])

@agenda_bp.route('/add', methods=['POST'])
def add():
    """ Rota para processar a criação de novas tarefas. """
    title = request.form.get('title')
    description = request.form.get('description')
    task_date = request.form.get('date')
    task_time = request.form.get('time')

    if not title or not task_date or not task_time:
        flash('Os campos Título, Data e Hora são obrigatórios!', 'error')
        return redirect(url_for('agenda.index'))

    try:
        task_model.add_task(title, description, task_date, task_time)
        flash('Tarefa agendada com sucesso!', 'success')
    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa: {e}")
        flash('Erro interno ao salvar tarefa.', 'error')
        
    return redirect(url_for('agenda.index'))

@agenda_bp.route('/complete/<task_id>')
def complete(task_id):
    """ Marca uma tarefa como finalizada. """
    if task_model.complete_task(task_id):
        flash('Tarefa concluída! Bom trabalho.', 'success')
    else:
        logger.warning(f"Tentativa falha de concluir tarefa inexistente: {task_id}")
        flash('Não foi possível encontrar a tarefa para concluir.', 'error')
    return redirect(url_for('agenda.index'))

@agenda_bp.route('/delete/<task_id>')
def delete(task_id):
    """ Remove uma tarefa após confirmação. """
    if task_model.delete_task(task_id):
        flash('Tarefa removida do sistema.', 'warning')
    else:
        logger.warning(f"Tentativa falha de remover tarefa: {task_id}")
        flash('Erro ao tentar remover a tarefa.', 'error')
    return redirect(url_for('agenda.index'))

