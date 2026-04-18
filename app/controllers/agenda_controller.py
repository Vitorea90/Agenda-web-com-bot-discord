from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import task_model

agenda_bp = Blueprint('agenda', __name__)

@agenda_bp.route('/')
def index():
    tasks = task_model.get_all_tasks()
    # Ordenar tarefas por data e hora
    tasks.sort(key=lambda x: (x['date'], x['time']))
    return render_template('index.html', tasks=tasks)

@agenda_bp.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    task_date = request.form.get('date')
    task_time = request.form.get('time')

    if not title or not task_date or not task_time:
        flash('Por favor, preencha todos os campos obrigatórios!', 'error')
        return redirect(url_for('agenda.index'))

    task_model.add_task(title, description, task_date, task_time)
    flash('Tarefa adicionada com sucesso!', 'success')
    return redirect(url_for('agenda.index'))

@agenda_bp.route('/complete/<task_id>')
def complete(task_id):
    if task_model.complete_task(task_id):
        flash('Tarefa marcada como concluída!', 'success')
    else:
        flash('Erro ao concluir tarefa.', 'error')
    return redirect(url_for('agenda.index'))

@agenda_bp.route('/delete/<task_id>')
def delete(task_id):
    if task_model.delete_task(task_id):
        flash('Tarefa removida.', 'warning')
    else:
        flash('Erro ao remover tarefa.', 'error')
    return redirect(url_for('agenda.index'))
