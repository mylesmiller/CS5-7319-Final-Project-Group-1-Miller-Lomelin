"""
Frontend Service - Microservices Architecture
Provides web interface for the microservices system.
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import requests
import csv
import io
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'frontend-service-secret-key')
CORS(app)

# Service URLs
TASK_SERVICE_URL = os.environ.get('TASK_SERVICE_URL', 'http://task-service:5000')
USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5001')

def get_from_service(url, endpoint):
    """Helper to get data from a service."""
    try:
        response = requests.get(f'{url}{endpoint}', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error calling {url}{endpoint}: {e}")
        return None

def post_to_service(url, endpoint, data):
    """Helper to post data to a service."""
    try:
        response = requests.post(
            f'{url}{endpoint}',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        return response
    except Exception as e:
        print(f"Error calling {url}{endpoint}: {e}")
        return None

def put_to_service(url, endpoint, data):
    """Helper to put data to a service."""
    try:
        response = requests.put(
            f'{url}{endpoint}',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        return response
    except Exception as e:
        print(f"Error calling {url}{endpoint}: {e}")
        return None

def delete_from_service(url, endpoint):
    """Helper to delete from a service."""
    try:
        response = requests.delete(f'{url}{endpoint}', timeout=5)
        return response
    except Exception as e:
        print(f"Error calling {url}{endpoint}: {e}")
        return None

@app.route('/')
def index():
    """Dashboard view."""
    # Get tasks
    tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks') or []
    
    # Get upcoming tasks and format as notifications
    upcoming_tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks/upcoming?days=7') or []
    notifications = []
    now = datetime.utcnow()
    
    for task in upcoming_tasks:
        if task.get('due_date'):
            try:
                due_date = datetime.fromisoformat(task['due_date'].replace('Z', '+00:00'))
                time_remaining = due_date - now
                total_seconds = int(time_remaining.total_seconds())
                days_until = time_remaining.days
                hours_until = total_seconds // 3600
                minutes_until = (total_seconds // 60) % 60
                seconds_until = total_seconds % 60
                
                # Format message based on time remaining
                if days_until > 0:
                    message = f'Task "{task.get("title", "Task")}" is due in {days_until} day(s)'
                elif hours_until > 0:
                    remaining_minutes = (total_seconds % 3600) // 60
                    if remaining_minutes > 0:
                        message = f'Task "{task.get("title", "Task")}" is due in {hours_until} hour(s), {remaining_minutes} minute(s)'
                    else:
                        message = f'Task "{task.get("title", "Task")}" is due in {hours_until} hour(s)'
                elif minutes_until > 0:
                    if seconds_until > 0:
                        message = f'Task "{task.get("title", "Task")}" is due in {minutes_until} minute(s), {seconds_until} second(s)'
                    else:
                        message = f'Task "{task.get("title", "Task")}" is due in {minutes_until} minute(s)'
                elif seconds_until > 0:
                    message = f'Task "{task.get("title", "Task")}" is due in {seconds_until} second(s)'
                else:
                    message = f'Task "{task.get("title", "Task")}" is overdue!'
                
                notifications.append({
                    'type': 'deadline_approaching',
                    'task_id': task.get('id'),
                    'task_title': task.get('title', 'Task'),
                    'due_date': task.get('due_date'),
                    'days_until': days_until,
                    'hours_until': hours_until,
                    'minutes_until': minutes_until,
                    'seconds_until': seconds_until,
                    'total_seconds': total_seconds,
                    'message': message
                })
            except Exception as e:
                print(f"Error processing task notification: {e}")
                continue
    
    # Get recent activity
    activity = get_from_service(TASK_SERVICE_URL, '/api/activity') or []
    
    return render_template('dashboard.html', 
                         tasks=tasks, 
                         notifications=notifications,
                         recent_activity=activity)

@app.route('/tasks')
def tasks():
    """Task list view."""
    tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks') or []
    users = get_from_service(USER_SERVICE_URL, '/api/users') or []
    return render_template('tasks.html', tasks=tasks, users=users)

@app.route('/calendar')
def calendar():
    """Calendar view."""
    tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks') or []
    return render_template('calendar.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """API endpoint to get all tasks."""
    tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks')
    if tasks is not None:
        return jsonify(tasks), 200
    return jsonify({'error': 'Task service unavailable'}), 503

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """API endpoint to create a task."""
    data = request.json
    response = post_to_service(TASK_SERVICE_URL, '/api/tasks', data)
    if response and response.status_code == 201:
        return jsonify(response.json()), 201
    return jsonify({'error': 'Failed to create task'}), response.status_code if response else 503

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """API endpoint to get a specific task."""
    task = get_from_service(TASK_SERVICE_URL, f'/api/tasks/{task_id}')
    if task is not None:
        return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """API endpoint to update a task."""
    data = request.json
    response = put_to_service(TASK_SERVICE_URL, f'/api/tasks/{task_id}', data)
    if response and response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Failed to update task'}), response.status_code if response else 503

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API endpoint to delete a task."""
    response = delete_from_service(TASK_SERVICE_URL, f'/api/tasks/{task_id}')
    if response and response.status_code == 200:
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete task'}), response.status_code if response else 503

@app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    """API endpoint to assign a task."""
    data = request.json
    response = post_to_service(TASK_SERVICE_URL, f'/api/tasks/{task_id}/assign', data)
    if response and response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Failed to assign task'}), response.status_code if response else 503

@app.route('/api/notifications')
def get_notifications():
    """API endpoint to get notifications."""
    notifications = get_from_service(NOTIFICATION_SERVICE_URL, '/api/notifications')
    if notifications is not None:
        return jsonify(notifications), 200
    return jsonify({'error': 'Notification service unavailable'}), 503

@app.route('/api/activity')
def get_activity():
    """API endpoint to get activity log."""
    activity = get_from_service(TASK_SERVICE_URL, '/api/activity')
    if activity is not None:
        return jsonify(activity), 200
    return jsonify({'error': 'Task service unavailable'}), 503

@app.route('/export/csv')
def export_csv():
    """Export tasks to CSV."""
    tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks') or []
    users = get_from_service(USER_SERVICE_URL, '/api/users') or []
    
    # Create user lookup
    user_lookup = {user['id']: user['username'] for user in users}
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Title', 'Description', 'Status', 'Priority', 
                    'Due Date', 'Assigned To', 'Created At', 'Updated At'])
    
    # Write data
    for task in tasks:
        assignee = user_lookup.get(task.get('assigned_to'), 'Unassigned')
        due_date = task.get('due_date', '')
        if due_date:
            try:
                dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                due_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
        
        created_at = task.get('created_at', '')
        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                created_at = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
        
        updated_at = task.get('updated_at', '')
        if updated_at:
            try:
                dt = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                updated_at = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
        
        writer.writerow([
            task.get('id', ''),
            task.get('title', ''),
            task.get('description', ''),
            task.get('status', ''),
            task.get('priority', ''),
            due_date,
            assignee,
            created_at,
            updated_at
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
    users = get_from_service(USER_SERVICE_URL, '/api/users')
    if users is not None:
        return jsonify(users), 200
    return jsonify({'error': 'User service unavailable'}), 503

@app.route('/api/users', methods=['POST'])
def create_user():
    """API endpoint to create a user."""
    data = request.json
    response = post_to_service(USER_SERVICE_URL, '/api/users', data)
    if response and response.status_code == 201:
        return jsonify(response.json()), 201
    return jsonify({'error': 'Failed to create user'}), response.status_code if response else 503

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'frontend-service'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)

