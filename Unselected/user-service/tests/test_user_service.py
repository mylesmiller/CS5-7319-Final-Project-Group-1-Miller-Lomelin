"""
Tests for User Service.
"""
import pytest
from app import app
from models import db, User

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

def test_create_user(client):
    """Test user creation."""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'

def test_get_user(client):
    """Test getting a user."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'testuser'

