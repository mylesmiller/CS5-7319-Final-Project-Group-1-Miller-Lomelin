"""
Task Service - Microservices Architecture
Manages all core task management functions.
Communicates with User Service for user-related operations.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from models import db, Task, ActivityLog
from config import Config
import os
import requests

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'task-service'}), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.json
    
    # Validate user IDs with User Service if provided
    if data.get('assigned_to'):
        if not validate_user_id(data['assigned_to']):
            return jsonify({'error': 'Invalid assigned_to user ID'}), 400
    
    if data.get('created_by'):
        if not validate_user_id(data['created_by']):
            return jsonify({'error': 'Invalid created_by user ID'}), 400
    
    due_date = None
    if data.get('due_date'):
        due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        due_date=due_date,
        assigned_to=data.get('assigned_to'),
        created_by=data.get('created_by')
    )
    
    db.session.add(task)
    db.session.commit()
    
    # Log activity
    activity = ActivityLog(
        task_id=task.id,
        action='created',
        description=f'Task "{data["title"]}" was created',
        user_id=data.get('created_by')
    )
    db.session.add(activity)
    db.session.commit()
    
    # Notify notification service (async simulation via event queue)
    notify_notification_service('task_created', {
        'task_id': task.id,
        'title': task.title,
        'assigned_to': task.assigned_to
    })
    
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task."""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    changes = []
    if 'title' in data and task.title != data['title']:
        changes.append(f"title changed from {task.title} to {data['title']}")
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data and task.status != data['status']:
        changes.append(f"status changed from {task.status} to {data['status']}")
        old_status = task.status
        task.status = data['status']
        # Notify on status change
        notify_notification_service('task_status_changed', {
            'task_id': task.id,
            'old_status': old_status,
            'new_status': data['status']
        })
    if 'priority' in data:
        task.priority = data['priority']
    if 'due_date' in data:
        new_due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data['due_date'] else None
        if task.due_date != new_due_date:
            changes.append(f"due_date changed")
        task.due_date = new_due_date
    if 'assigned_to' in data:
        # Validate user ID if provided
        if data['assigned_to'] and not validate_user_id(data['assigned_to']):
            return jsonify({'error': 'Invalid assigned_to user ID'}), 400
        task.assigned_to = data['assigned_to']
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Log activity
    if changes:
        activity = ActivityLog(
            task_id=task.id,
            action='updated',
            description='; '.join(changes),
            user_id=data.get('updated_by')
        )
        db.session.add(activity)
        db.session.commit()
    
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    """Assign a task to a user."""
    task = Task.query.get_or_404(task_id)
    data = request.json
    user_id = data['user_id']
    
    # Validate user exists in User Service
    user = get_user_from_service(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    task.assigned_to = user_id
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Log activity
    activity = ActivityLog(
        task_id=task.id,
        action='assigned',
        description=f'Task assigned to {user["username"]}',
        user_id=data.get('assigned_by')
    )
    db.session.add(activity)
    db.session.commit()
    
    # Notify notification service
    notify_notification_service('task_assigned', {
        'task_id': task.id,
        'task_title': task.title,
        'assigned_to': user_id,
        'user_email': user['email']
    })
    
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks/upcoming', methods=['GET'])
def get_upcoming_tasks():
    """Get tasks with upcoming deadlines."""
    from datetime import timedelta
    days = request.args.get('days', 7, type=int)
    cutoff_date = datetime.utcnow() + timedelta(days=days)
    
    tasks = Task.query.filter(
        Task.due_date <= cutoff_date,
        Task.due_date >= datetime.utcnow(),
        Task.status != 'completed'
    ).all()
    
    return jsonify([task.to_dict() for task in tasks]), 200

@app.route('/api/activity', methods=['GET'])
def get_activity():
    """Get activity log."""
    limit = request.args.get('limit', 50, type=int)
    activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    
    return jsonify([{
        'id': activity.id,
        'task_id': activity.task_id,
        'action': activity.action,
        'description': activity.description,
        'created_at': activity.created_at.isoformat()
    } for activity in activities]), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users from User Service."""
    return get_users_from_service()

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user from User Service."""
    user = get_user_from_service(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

def get_user_from_service(user_id):
    """Get a user from User Service."""
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    
    try:
        response = requests.get(
            f'{user_service_url}/api/users/{user_id}',
            timeout=2
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Failed to get user from User Service: {e}")
        return None

def get_users_from_service():
    """Get all users from User Service."""
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    
    try:
        response = requests.get(
            f'{user_service_url}/api/users',
            timeout=2
        )
        if response.status_code == 200:
            return response.json(), 200
        return jsonify({'error': 'Failed to fetch users'}), 500
    except Exception as e:
        print(f"Failed to get users from User Service: {e}")
        return jsonify({'error': 'User Service unavailable'}), 503

def validate_user_id(user_id):
    """Validate that a user ID exists in User Service."""
    user = get_user_from_service(user_id)
    return user is not None

def notify_notification_service(event_type, payload):
    """
    Notify the notification service about an event.
    In a real implementation, this would use a message queue or HTTP call.
    For simplicity, we'll use HTTP with error handling.
    """
    notification_service_url = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5001')
    
    try:
        import requests
        requests.post(
            f'{notification_service_url}/api/events',
            json={
                'event_type': event_type,
                'payload': payload,
                'timestamp': datetime.utcnow().isoformat()
            },
            timeout=2
        )
    except Exception as e:
        # Log error but don't fail the request
        print(f"Failed to notify notification service: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

