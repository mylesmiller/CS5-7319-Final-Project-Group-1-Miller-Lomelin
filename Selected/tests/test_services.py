"""
Unit tests for service layer.
"""
import pytest
from datetime import datetime, timedelta
from app import create_app
from models import db, User, Task
from services.task_service import TaskService

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_create_task(app):
    """Test task creation service."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        task = TaskService.create_task(
            title='New Task',
            description='Task Description',
            priority='high',
            created_by=user.id
        )
        
        assert task.id is not None
        assert task.title == 'New Task'
        assert len(task.activities) > 0

def test_update_task(app):
    """Test task update service."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        task = TaskService.create_task(
            title='Original Title',
            created_by=user.id
        )
        
        updated_task = TaskService.update_task(task.id, title='Updated Title')
        assert updated_task.title == 'Updated Title'

