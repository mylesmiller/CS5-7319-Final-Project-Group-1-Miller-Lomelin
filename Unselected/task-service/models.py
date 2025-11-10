"""
Data models for Task Service.
Note: User data is managed by the User Service, so we only store user IDs as integers.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    """Task model."""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='medium')
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Store user IDs as integers (users are managed by User Service)
    assigned_to = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.Integer, nullable=True)
    
    activities = db.relationship('ActivityLog', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def to_dict(self, include_username=False, user_service_url=None):
        """Convert task to dictionary."""
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'assigned_to': self.assigned_to,
            'created_by': self.created_by
        }
        
        # Optionally include username if requested and user_id exists
        if include_username and self.assigned_to and user_service_url:
            try:
                import requests
                response = requests.get(f'{user_service_url}/api/users/{self.assigned_to}', timeout=1)
                if response.status_code == 200:
                    user = response.json()
                    result['assigned_to_username'] = user.get('username')
            except:
                pass  # Silently fail if user service is unavailable
        
        return result

class ActivityLog(db.Model):
    """Activity log model."""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    # Store user ID as integer (users are managed by User Service)
    user_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActivityLog {self.action} for Task {self.task_id}>'

