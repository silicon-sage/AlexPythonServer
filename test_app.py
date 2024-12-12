import pytest
from main import app
import json
from datetime import datetime
from freezegun import freeze_time

@pytest.fixture
def client():
    """Configure Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page returns HTML with expected content"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Simple Todo App' in response.data
    assert b'/api/todos' in response.data

def test_create_todo(client):
    """Test creating a new todo"""
    response = client.post(
        '/api/todos',
        data=json.dumps({'task': 'Test task'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['task'] == 'Test task'
    assert data['id'] > -1
    assert not data['completed']
    assert 'created_at' in data

def test_create_todo_invalid_content_type(client):
    """Test creating todo with wrong content type"""
    response = client.post(
        '/api/todos',
        data='{"task": "Test task"}'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Content-Type must be application/json'

def test_create_todo_missing_task(client):
    """Test creating todo without task field"""
    response = client.post(
        '/api/todos',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'task field is required'

def test_create_and_get_todos(client):
    """Test creating multiple todos and retrieving them"""
    # Create first todo
    response1 = client.post(
        '/api/todos',
        data=json.dumps({'task': 'First task'}),
        content_type='application/json'
    )
    assert response1.status_code == 201

    # Create second todo
    response2 = client.post(
        '/api/todos',
        data=json.dumps({'task': 'Second task'}),
        content_type='application/json'
    )
    assert response2.status_code == 201

    # Get all todos
    response = client.get('/api/todos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 2
