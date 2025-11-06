"""
Database repositories - Data access layer.
This layer abstracts database operations from the business logic.
"""
from models import db, Task, User, ActivityLog
from typing import List, Optional
from datetime import datetime

class TaskRepository:
    """Repository for Task data access operations."""
    
    @staticmethod
    def create(title: str, description: str = None, priority: str = 'medium', 
               due_date: datetime = None, assigned_to: int = None, created_by: int = None) -> Task:
        """Create a new task in the database."""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to,
            created_by=created_by
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def get_by_id(task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return Task.query.get(task_id)
    
    @staticmethod
    def get_by_id_or_404(task_id: int) -> Task:
        """Get a task by ID or raise 404."""
        return Task.query.get_or_404(task_id)
    
    @staticmethod
    def get_all() -> List[Task]:
        """Get all tasks."""
        return Task.query.all()
    
    @staticmethod
    def get_by_user(user_id: int) -> List[Task]:
        """Get all tasks assigned to a user."""
        return Task.query.filter_by(assigned_to=user_id).all()
    
    @staticmethod
    def get_upcoming_deadlines(days: int = 7) -> List[Task]:
        """Get tasks with upcoming deadlines."""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() + timedelta(days=days)
        return Task.query.filter(
            Task.due_date <= cutoff_date,
            Task.due_date >= datetime.utcnow(),
            Task.status != 'completed'
        ).all()
    
    @staticmethod
    def update(task: Task, **kwargs) -> Task:
        """Update task fields."""
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        db.session.commit()
        return task
    
    @staticmethod
    def delete(task_id: int) -> bool:
        """Delete a task."""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return True
    
    @staticmethod
    def save(task: Task) -> Task:
        """Save task changes to database."""
        db.session.commit()
        return task

class UserRepository:
    """Repository for User data access operations."""
    
    @staticmethod
    def create(username: str, email: str) -> User:
        """Create a new user in the database."""
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_id_or_404(user_id: int) -> User:
        """Get a user by ID or raise 404."""
        return User.query.get_or_404(user_id)
    
    @staticmethod
    def get_all() -> List[User]:
        """Get all users."""
        return User.query.all()
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """Get a user by username."""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get a user by email."""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def update(user: User, **kwargs) -> User:
        """Update user fields."""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id: int) -> bool:
        """Delete a user."""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return True

class ActivityLogRepository:
    """Repository for ActivityLog data access operations."""
    
    @staticmethod
    def create(task_id: int, action: str, description: str = None, user_id: int = None) -> ActivityLog:
        """Create a new activity log entry."""
        activity = ActivityLog(
            task_id=task_id,
            action=action,
            description=description,
            user_id=user_id
        )
        db.session.add(activity)
        db.session.commit()
        return activity
    
    @staticmethod
    def get_by_task_id(task_id: int) -> List[ActivityLog]:
        """Get all activity logs for a task."""
        return ActivityLog.query.filter_by(task_id=task_id).order_by(ActivityLog.created_at.desc()).all()
    
    @staticmethod
    def get_recent(limit: int = 50) -> List[ActivityLog]:
        """Get recent activity logs."""
        return ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_all() -> List[ActivityLog]:
        """Get all activity logs."""
        return ActivityLog.query.order_by(ActivityLog.created_at.desc()).all()

