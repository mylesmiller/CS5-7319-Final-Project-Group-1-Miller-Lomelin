"""
Business logic for task management operations.
Uses the database layer (repositories) for data access.
"""
from datetime import datetime
from database.repositories import TaskRepository, UserRepository, ActivityLogRepository

class TaskService:
    """Service layer for task operations."""
    
    @staticmethod
    def _format_field_name(field_name):
        """Convert field names to user-friendly format."""
        field_map = {
            'due_date': 'due date',
            'assigned_to': 'assigned to',
            'created_by': 'created by',
            'updated_by': 'updated by'
        }
        return field_map.get(field_name, field_name.replace('_', ' '))
    
    @staticmethod
    def _format_value(value, field_name=''):
        """Format values for display in activity logs."""
        if value is None:
            return 'not set'
        if isinstance(value, datetime):
            # Format datetime as readable date and time
            return value.strftime('%B %d, %Y at %I:%M %p')
        if field_name == 'assigned_to':
            # Handle user assignment - value could be int (user_id) or User object
            user_id = value
            if hasattr(value, 'id'):
                user_id = value.id
            if isinstance(user_id, int):
                # Try to get username if it's a user ID
                try:
                    user = UserRepository.get_by_id(user_id)
                    return user.username if user else f'user {user_id}'
                except:
                    return f'user {user_id}'
        return str(value)
    
    @staticmethod
    def create_task(title, description, priority='medium', due_date=None, assigned_to=None, created_by=None):
        """Create a new task."""
        # Use repository for data access
        task = TaskRepository.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to,
            created_by=created_by
        )
        
        # Log activity using repository
        ActivityLogRepository.create(
            task_id=task.id,
            action='created',
            description=f'Task "{title}" was created',
            user_id=created_by
        )
        
        return task
    
    @staticmethod
    def update_task(task_id, **kwargs):
        """Update an existing task."""
        # Get task using repository
        task = TaskRepository.get_by_id_or_404(task_id)
        
        # Track changes for activity log
        changes = []
        update_data = {}
        
        for key, value in kwargs.items():
            if hasattr(task, key) and getattr(task, key) != value:
                old_value = getattr(task, key)
                update_data[key] = value
                
                # Format the change message
                field_name = TaskService._format_field_name(key)
                old_formatted = TaskService._format_value(old_value, key)
                new_formatted = TaskService._format_value(value, key)
                changes.append(f"{field_name} was changed from {old_formatted} to {new_formatted}")
        
        # Update using repository
        if update_data:
            task = TaskRepository.update(task, **update_data)
        
        # Log activity if there were changes
        if changes:
            ActivityLogRepository.create(
                task_id=task.id,
                action='updated',
                description='; '.join(changes),
                user_id=kwargs.get('updated_by')
            )
        
        return task
    
    @staticmethod
    def assign_task(task_id, user_id, assigned_by=None):
        """Assign a task to a user, or unassign if user_id is None."""
        # Get task using repository
        task = TaskRepository.get_by_id_or_404(task_id)
        
        old_assignee = task.assignee.username if task.assignee else None
        
        # Update assignment using repository
        task = TaskRepository.update(task, assigned_to=user_id)
        
        # Log activity using repository
        if user_id is None:
            # Unassignment
            description = 'Task unassigned' if old_assignee else 'Task remains unassigned'
            ActivityLogRepository.create(
                task_id=task.id,
                action='updated',
                description=description,
                user_id=assigned_by
            )
        else:
            # Assignment
            user = UserRepository.get_by_id_or_404(user_id)
            description = f'Task assigned to {user.username}'
            if old_assignee:
                description = f'Task reassigned from {old_assignee} to {user.username}'
            ActivityLogRepository.create(
                task_id=task.id,
                action='assigned',
                description=description,
                user_id=assigned_by
            )
        
        return task
    
    @staticmethod
    def get_all_tasks():
        """Get all tasks."""
        return TaskRepository.get_all()
    
    @staticmethod
    def get_task_by_id(task_id):
        """Get a task by ID."""
        return TaskRepository.get_by_id_or_404(task_id)
    
    @staticmethod
    def get_tasks_by_user(user_id):
        """Get all tasks assigned to a user."""
        return TaskRepository.get_by_user(user_id)
    
    @staticmethod
    def get_upcoming_deadlines(days=7):
        """Get tasks with upcoming deadlines."""
        return TaskRepository.get_upcoming_deadlines(days)
    
    @staticmethod
    def delete_task(task_id):
        """Delete a task."""
        return TaskRepository.delete(task_id)

