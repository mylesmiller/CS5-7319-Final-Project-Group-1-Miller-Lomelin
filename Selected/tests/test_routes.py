"""
Integration tests for routes.
"""
import pytest
import json
from app import create_app
from models import db, User, Task

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

def test_get_tasks(client):
    """Test GET /api/tasks endpoint."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_task(client, app):
    """Test POST /api/tasks endpoint."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        task_data = {
            'title': 'New Task',
            'description': 'Task Description',
            'priority': 'medium',
            'created_by': user.id
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'New Task'

