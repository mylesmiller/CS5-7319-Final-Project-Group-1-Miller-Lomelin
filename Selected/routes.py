"""
Route handlers (Controller layer).
"""
from flask import render_template, request, jsonify, redirect, url_for, send_file
from models import db, Task, User, ActivityLog
from database.repositories import UserRepository, ActivityLogRepository
from services.task_service import TaskService
from services.notification_service import NotificationService
import csv
import io
from datetime import datetime

def register_routes(app):
    """Register all routes with the Flask app."""
    
    @app.route('/')
    def index():
        """Dashboard view."""
        tasks = TaskService.get_all_tasks()
        notifications = NotificationService.check_upcoming_deadlines()
        recent_activity = NotificationService.get_recent_activity()
        return render_template('dashboard.html', 
                             tasks=tasks, 
                             notifications=notifications,
                             recent_activity=recent_activity)
    
    @app.route('/tasks')
    def tasks():
        """Task list view."""
        tasks = TaskService.get_all_tasks()
        users = UserRepository.get_all()
        return render_template('tasks.html', tasks=tasks, users=users)
    
    @app.route('/calendar')
    def calendar():
        """Calendar view."""
        tasks = TaskService.get_all_tasks()
        # Convert tasks to dictionaries for JSON serialization
        tasks_dict = [task.to_dict() for task in tasks]
        return render_template('calendar.html', tasks=tasks_dict)
    
    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        """API endpoint to get all tasks."""
        tasks = TaskService.get_all_tasks()
        return jsonify([task.to_dict() for task in tasks])
    
    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """API endpoint to create a task."""
        data = request.json
        due_date = None
        if data.get('due_date'):
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        
        task = TaskService.create_task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            due_date=due_date,
            assigned_to=data.get('assigned_to'),
            created_by=data.get('created_by')
        )
        return jsonify(task.to_dict()), 201
    
    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """API endpoint to get a specific task."""
        task = TaskService.get_task_by_id(task_id)
        return jsonify(task.to_dict())
    
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """API endpoint to update a task."""
        data = request.json
        update_data = {}
        
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'status' in data:
            update_data['status'] = data['status']
        if 'priority' in data:
            update_data['priority'] = data['priority']
        if 'due_date' in data:
            update_data['due_date'] = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data['due_date'] else None
        if 'assigned_to' in data:
            update_data['assigned_to'] = data['assigned_to']
        
        task = TaskService.update_task(task_id, **update_data)
        return jsonify(task.to_dict())
    
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """API endpoint to delete a task."""
        TaskService.delete_task(task_id)
        return jsonify({'message': 'Task deleted successfully'}), 200
    
    @app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
    def assign_task(task_id):
        """API endpoint to assign a task."""
        data = request.json
        task = TaskService.assign_task(task_id, data['user_id'], assigned_by=data.get('assigned_by'))
        return jsonify(task.to_dict())
    
    @app.route('/api/notifications')
    def get_notifications():
        """API endpoint to get notifications."""
        notifications = NotificationService.check_upcoming_deadlines()
        return jsonify(notifications)
    
    @app.route('/api/activity')
    def get_activity():
        """API endpoint to get activity log."""
        activities = ActivityLogRepository.get_recent(50)
        return jsonify([{
            'id': activity.id,
            'task_id': activity.task_id,
            'action': activity.action,
            'description': activity.description,
            'created_at': activity.created_at.isoformat()
        } for activity in activities])
    
    @app.route('/export/csv')
    def export_csv():
        """Export tasks to CSV."""
        tasks = TaskService.get_all_tasks()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Title', 'Description', 'Status', 'Priority', 
                        'Due Date', 'Assigned To', 'Created At', 'Updated At'])
        
        # Write data
        for task in tasks:
            assignee = task.assignee.username if task.assignee else 'Unassigned'
            due_date = task.due_date.strftime('%Y-%m-%d %H:%M:%S') if task.due_date else ''
            writer.writerow([
                task.id,
                task.title,
                task.description or '',
                task.status,
                task.priority,
                due_date,
                assignee,
                task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'tasks_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """API endpoint to get all users."""
        users = UserRepository.get_all()
        return jsonify([{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in users])
    
    @app.route('/api/users', methods=['POST'])
    def create_user():
        """API endpoint to create a user."""
        data = request.json
        user = UserRepository.create(
            username=data['username'],
            email=data['email']
        )
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 201

