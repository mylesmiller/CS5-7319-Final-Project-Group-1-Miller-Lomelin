"""
Unit tests for data models.
"""
import pytest
from datetime import datetime
from app import create_app
from models import db, User, Task, ActivityLog

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

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_user_creation(app):
    """Test user creation."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'

def test_task_creation(app):
    """Test task creation."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        task = Task(
            title='Test Task',
            description='Test Description',
            priority='high',
            created_by=user.id
        )
        db.session.add(task)
        db.session.commit()
        
        assert task.id is not None
        assert task.title == 'Test Task'
        assert task.status == 'pending'

