"""
Tests for Task Service.
"""
import pytest
from app import app
from models import db, User, Task

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_create_task(client):
    """Test task creation."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
            'created_by': user.id
        }
        
        response = client.post('/api/tasks', json=task_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Test Task'

