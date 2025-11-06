"""
Notification service for in-app notifications.
Uses the database layer (repositories) for data access.
"""
from datetime import datetime, timedelta
from database.repositories import TaskRepository, ActivityLogRepository

class NotificationService:
    """Service for handling notifications."""
    
    @staticmethod
    def check_upcoming_deadlines(days=7):
        """Check for tasks with upcoming deadlines and return notifications."""
        notifications = []
        
        # Use repository for data access
        upcoming_tasks = TaskRepository.get_upcoming_deadlines(days)
        now = datetime.utcnow()
        
        for task in upcoming_tasks:
            time_remaining = task.due_date - now
            
            # Calculate time components
            total_seconds = int(time_remaining.total_seconds())
            days_until = time_remaining.days
            hours_until = total_seconds // 3600  # Total hours (not modulo 24)
            minutes_until = (total_seconds // 60) % 60
            seconds_until = total_seconds % 60
            
            # Format message based on time remaining
            if days_until > 0:
                message = f'Task "{task.title}" is due in {days_until} day(s)'
            elif hours_until > 0:
                remaining_minutes = (total_seconds % 3600) // 60
                if remaining_minutes > 0:
                    message = f'Task "{task.title}" is due in {hours_until} hour(s), {remaining_minutes} minute(s)'
                else:
                    message = f'Task "{task.title}" is due in {hours_until} hour(s)'
            elif minutes_until > 0:
                if seconds_until > 0:
                    message = f'Task "{task.title}" is due in {minutes_until} minute(s), {seconds_until} second(s)'
                else:
                    message = f'Task "{task.title}" is due in {minutes_until} minute(s)'
            elif seconds_until > 0:
                message = f'Task "{task.title}" is due in {seconds_until} second(s)'
            else:
                message = f'Task "{task.title}" is overdue!'
            
            notifications.append({
                'type': 'deadline_approaching',
                'task_id': task.id,
                'task_title': task.title,
                'due_date': task.due_date.isoformat(),
                'days_until': days_until,
                'hours_until': hours_until,
                'minutes_until': minutes_until,
                'seconds_until': seconds_until,
                'total_seconds': total_seconds,
                'message': message
            })
        
        return notifications
    
    @staticmethod
    def get_recent_activity(limit=10):
        """Get recent activity for notifications."""
        # Use repository for data access
        activities = ActivityLogRepository.get_recent(limit)
        
        return [{
            'id': activity.id,
            'task_id': activity.task_id,
            'action': activity.action,
            'description': activity.description,
            'created_at': activity.created_at.isoformat()
        } for activity in activities]

