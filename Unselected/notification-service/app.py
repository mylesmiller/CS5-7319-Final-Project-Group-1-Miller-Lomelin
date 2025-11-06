"""
Notification Service - Microservices Architecture
Handles all notifications and alerts.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'notification-service-secret-key')
CORS(app)

# In-memory storage for notifications (in production, use a proper database)
notifications = []

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'notification-service'}), 200

@app.route('/api/events', methods=['POST'])
def handle_event():
    """Handle events from other services."""
    data = request.json
    event_type = data.get('event_type')
    payload = data.get('payload', {})
    
    # Process different event types
    if event_type == 'task_created':
        send_notification({
            'type': 'task_created',
            'message': f'New task created: {payload.get("title")}',
            'task_id': payload.get('task_id'),
            'assigned_to': payload.get('assigned_to')
        })
    elif event_type == 'task_assigned':
        send_notification({
            'type': 'task_assigned',
            'message': f'Task "{payload.get("task_title")}" has been assigned to you',
            'task_id': payload.get('task_id'),
            'user_email': payload.get('user_email')
        })
    elif event_type == 'task_status_changed':
        send_notification({
            'type': 'status_changed',
            'message': f'Task status changed from {payload.get("old_status")} to {payload.get("new_status")}',
            'task_id': payload.get('task_id')
        })
    
    return jsonify({'status': 'processed'}), 200

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Get all notifications."""
    limit = request.args.get('limit', 50, type=int)
    return jsonify(notifications[:limit]), 200

@app.route('/api/notifications/upcoming-deadlines', methods=['POST'])
def check_upcoming_deadlines():
    """
    Check for upcoming deadlines.
    This endpoint is called by a scheduler or the task service.
    """
    data = request.json
    tasks = data.get('tasks', [])
    
    upcoming_notifications = []
    for task in tasks:
        if task.get('due_date') and task.get('status') != 'completed':
            # Parse due date and check if it's within 7 days
            due_date = datetime.fromisoformat(task['due_date'].replace('Z', '+00:00'))
            days_until = (due_date - datetime.utcnow()).days
            
            if 0 <= days_until <= 7:
                notification = {
                    'type': 'deadline_approaching',
                    'task_id': task['id'],
                    'task_title': task['title'],
                    'due_date': task['due_date'],
                    'days_until': days_until,
                    'message': f'Task "{task["title"]}" is due in {days_until} day(s)'
                }
                upcoming_notifications.append(notification)
                send_notification(notification)
    
    return jsonify(upcoming_notifications), 200

def send_notification(notification_data):
    """
    Send a notification.
    In production, this would send emails, push notifications, etc.
    For now, we'll store them in memory and optionally send emails if configured.
    """
    notification = {
        **notification_data,
        'timestamp': datetime.utcnow().isoformat(),
        'sent': False
    }
    
    # Store notification
    notifications.append(notification)
    
    # If email is configured and user_email is provided, send email
    if notification_data.get('user_email') and os.environ.get('SMTP_ENABLED') == 'true':
        try:
            send_email_notification(
                notification_data['user_email'],
                notification_data.get('message', 'Notification'),
                notification_data.get('message', 'You have a new notification')
            )
            notification['sent'] = True
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    # In a real system, you might also send push notifications, SMS, etc.
    print(f"Notification: {notification_data.get('message')}")

def send_email_notification(to_email, subject, body):
    """Send an email notification (mock implementation)."""
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    if not smtp_user or not smtp_password:
        print("SMTP not configured, skipping email send")
        return
    
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # In production, actually send the email
    # For now, just log it
    print(f"Would send email to {to_email}: {subject}")

@app.route('/api/notifications/clear', methods=['POST'])
def clear_notifications():
    """Clear all notifications (for testing)."""
    global notifications
    notifications = []
    return jsonify({'message': 'Notifications cleared'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

