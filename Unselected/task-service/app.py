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

# Helper functions for formatting
def format_field_name(field_name):
    """Convert field names to user-friendly format."""
    field_map = {
        'due_date': 'due date',
        'assigned_to': 'assigned to',
        'created_by': 'created by',
        'updated_by': 'updated by'
    }
    return field_map.get(field_name, field_name.replace('_', ' '))

def format_value(value, field_name='', user_service_url=None):
    """Format values for display in activity logs."""
    if value is None:
        return 'not set'
    if isinstance(value, datetime):
        # Format datetime as readable date and time
        return value.strftime('%B %d, %Y at %I:%M %p')
    if field_name == 'assigned_to':
        # Handle user assignment - value is user_id (int)
        if isinstance(value, int):
            # Try to get username from User Service
            try:
                user = get_user_from_service(value)
                return user['username'] if user else f'user {value}'
            except:
                return f'user {value}'
    return str(value)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'task-service'}), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    tasks = Task.query.all()
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    include_username = request.args.get('include_username', 'false').lower() == 'true'
    return jsonify([task.to_dict(include_username=include_username, user_service_url=user_service_url) for task in tasks]), 200

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
    
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    include_username = request.args.get('include_username', 'false').lower() == 'true'
    return jsonify(task.to_dict(include_username=include_username, user_service_url=user_service_url)), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task."""
    task = Task.query.get_or_404(task_id)
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    include_username = request.args.get('include_username', 'false').lower() == 'true'
    return jsonify(task.to_dict(include_username=include_username, user_service_url=user_service_url)), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    task = Task.query.get_or_404(task_id)
    data = request.json
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    
    changes = []
    update_data = {}
    
    # Track old status for notification
    old_status_for_notification = None
    
    # Track changes for activity log
    for key, value in data.items():
        if key in ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']:
            old_value = getattr(task, key, None)
            
            # Handle special cases
            if key == 'due_date':
                new_value = datetime.fromisoformat(value.replace('Z', '+00:00')) if value else None
            elif key == 'assigned_to':
                # Validate user ID if provided
                if value and not validate_user_id(value):
                    return jsonify({'error': 'Invalid assigned_to user ID'}), 400
                new_value = value
            else:
                new_value = value
            
            # Check if value actually changed
            if old_value != new_value:
                update_data[key] = new_value
                
                # Store old status for notification
                if key == 'status':
                    old_status_for_notification = old_value
                
                # Format the change message
                field_name = format_field_name(key)
                old_formatted = format_value(old_value, key, user_service_url)
                new_formatted = format_value(new_value, key, user_service_url)
                changes.append(f"{field_name} was changed from {old_formatted} to {new_formatted}")
    
    # Apply updates
    for key, value in update_data.items():
        if key == 'due_date':
            task.due_date = value
        elif key == 'assigned_to':
            task.assigned_to = value
        else:
            setattr(task, key, value)
    
    # Notify on status change
    if 'status' in update_data and old_status_for_notification:
        notify_notification_service('task_status_changed', {
            'task_id': task.id,
            'old_status': old_status_for_notification.replace('_', ' ').title(),
            'new_status': update_data['status']
        })
    
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
    
    include_username = request.args.get('include_username', 'false').lower() == 'true'
    return jsonify(task.to_dict(include_username=include_username, user_service_url=user_service_url)), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    """Assign a task to a user, or unassign if user_id is None."""
    task = Task.query.get_or_404(task_id)
    data = request.json
    user_id = data.get('user_id')  # Can be None for unassignment
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    
    old_assigned = task.assigned_to
    old_user = None
    if old_assigned:
        old_user = get_user_from_service(old_assigned)
    
    if user_id is None:
        # Unassignment
        task.assigned_to = None
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        description = 'Task unassigned' if old_user else 'Task remains unassigned'
        if old_user:
            description = f'Task unassigned from {old_user["username"]}'
        
        activity = ActivityLog(
            task_id=task.id,
            action='updated',
            description=description,
            user_id=data.get('assigned_by')
        )
        db.session.add(activity)
        db.session.commit()
    else:
        # Assignment
        user = get_user_from_service(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        task.assigned_to = user_id
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log activity
        if old_user:
            description = f'Task reassigned from {old_user["username"]} to {user["username"]}'
        else:
            description = f'Task assigned to {user["username"]}'
        
        activity = ActivityLog(
            task_id=task.id,
            action='assigned',
            description=description,
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
    
    include_username = request.args.get('include_username', 'false').lower() == 'true'
    return jsonify(task.to_dict(include_username=include_username, user_service_url=user_service_url)), 200

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

