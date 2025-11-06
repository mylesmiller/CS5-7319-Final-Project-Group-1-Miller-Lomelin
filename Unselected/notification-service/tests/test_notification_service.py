"""
Tests for Notification Service.
"""
import pytest
from app import app

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    return app.test_client()

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_handle_event(client):
    """Test event handling."""
    event_data = {
        'event_type': 'task_created',
        'payload': {
            'task_id': 1,
            'title': 'Test Task'
        }
    }
    
    response = client.post('/api/events', json=event_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'processed'

