import pytest
import json
import os
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Set test environment variables
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_NAME'] = 'test_db'
    os.environ['DB_USER'] = 'test_user'
    os.environ['DB_PASSWORD'] = 'test_password'
    os.environ['DB_PORT'] = '5432'
    
    # Return the app for testing
    return flask_app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['message'] == 'Welcome to Flask Kubernetes Demo'
    assert data['status'] == 'running'

def test_health_route(client):
    """Test the health check route."""
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'healthy'

def test_db_test_route_mock(client, monkeypatch):
    """Test the database test route with mocked connection."""
    # This test mocks the database connection to avoid needing a real database
    
    class MockCursor:
        def execute(self, query):
            pass
            
        def fetchone(self):
            return {'version': 'PostgreSQL 13.0'}
            
        def close(self):
            pass
    
    class MockConnection:
        def cursor(self):
            return MockCursor()
            
        def close(self):
            pass
    
    # Mock the get_db_connection function
    def mock_get_db_connection():
        return MockConnection()
        
    # Apply the monkeypatch
    monkeypatch.setattr('app.get_db_connection', mock_get_db_connection)
    
    # Test the route
    response = client.get('/db-test')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Database connection successful'
    assert 'version' in data

def test_tasks_get_route_mock(client, monkeypatch):
    """Test the tasks GET route with mocked connection."""
    
    class MockCursor:
        def execute(self, query):
            pass
            
        def fetchall(self):
            return [
                {'id': 1, 'title': 'Task 1', 'description': 'Description 1'},
                {'id': 2, 'title': 'Task 2', 'description': 'Description 2'}
            ]
            
        def close(self):
            pass
    
    class MockConnection:
        def cursor(self):
            return MockCursor()
            
        def close(self):
            pass
    
    # Mock the get_db_connection function
    def mock_get_db_connection():
        return MockConnection()
        
    # Apply the monkeypatch
    monkeypatch.setattr('app.get_db_connection', mock_get_db_connection)
    
    # Test the route
    response = client.get('/tasks')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['tasks']) == 2
    assert data['tasks'][0]['title'] == 'Task 1'
    assert data['tasks'][1]['title'] == 'Task 2'

def test_tasks_post_route_mock(client, monkeypatch):
    """Test the tasks POST route with mocked connection."""
    
    class MockCursor:
        def execute(self, query, params=None):
            pass
            
        def fetchone(self):
            return {'id': 3, 'title': 'New Task', 'description': 'New Description'}
            
        def close(self):
            pass
    
    class MockConnection:
        def cursor(self):
            return MockCursor()
            
        def commit(self):
            pass
            
        def close(self):
            pass
    
    # Mock the get_db_connection function
    def mock_get_db_connection():
        return MockConnection()
        
    # Apply the monkeypatch
    monkeypatch.setattr('app.get_db_connection', mock_get_db_connection)
    
    # Test the route
    response = client.post(
        '/tasks',
        data=json.dumps({'title': 'New Task', 'description': 'New Description'}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['message'] == 'Task created successfully'
    assert data['task']['title'] == 'New Task'
    assert data['task']['description'] == 'New Description'

def test_tasks_post_route_missing_title(client):
    """Test the tasks POST route with missing title."""
    response = client.post(
        '/tasks',
        data=json.dumps({'description': 'New Description'}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert data['message'] == 'Title is required'
