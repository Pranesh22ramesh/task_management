from flask import Blueprint, request, jsonify, render_template, Response
from flask_login import login_required, current_user
from models.task import Task, db
from services.websocket_service import notify_event
from services.analytics_service import export_tasks_csv
from datetime import datetime

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@task_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_date.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200

@task_bp.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    due_date_str = data.get('due_date')

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError:
            pass

    if not title:
        return jsonify({"success": False, "message": "Title is required"}), 400

    new_task = Task(
        title=title, description=description, priority=priority,
        due_date=due_date, user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()

    task_data = new_task.to_dict()
    notify_event('task_added', task_data)

    return jsonify({"success": True, "message": "Task added successfully", "task": task_data}), 201

@task_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    
    if data.get('due_date'):
        try:
            task.due_date = datetime.fromisoformat(data.get('due_date'))
        except ValueError:
            pass

    db.session.commit()
    task_data = task.to_dict()
    notify_event('task_updated', task_data)
    
    if task.status == 'Completed':
        notify_event('task_completed', task_data)

    return jsonify({"success": True, "message": "Task updated", "task": task_data}), 200

@task_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    notify_event('task_deleted', {'id': task_id})

    return jsonify({"success": True, "message": "Task deleted"}), 200

@task_bp.route('/api/tasks/export')
@login_required
def export_tasks():
    csv_data = export_tasks_csv(current_user.id)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=tasks.csv"}
    )
