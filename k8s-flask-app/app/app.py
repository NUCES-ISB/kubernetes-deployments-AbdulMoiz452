from flask import Flask, jsonify, request
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '5432')

def get_db_connection():
    """Create a database connection"""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )
    return conn

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Welcome to Flask Kubernetes Demo',
        'status': 'running'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy'
    })

@app.route('/db-test')
def db_test():
    """Test database connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()['version']
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Database connection successful',
            'version': version
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}'
        }), 500

@app.route('/init-db')
def init_db():
    """Initialize database with a sample table and data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create a sample table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Insert some sample data
        cursor.execute('''
            INSERT INTO tasks (title, description)
            VALUES 
                ('Task 1', 'Description for task 1'),
                ('Task 2', 'Description for task 2'),
                ('Task 3', 'Description for task 3')
            ON CONFLICT DO NOTHING;
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Database initialized with sample data'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database initialization failed: {str(e)}'
        }), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY id;')
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'tasks': tasks
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to retrieve tasks: {str(e)}'
        }), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        
        if not title:
            return jsonify({
                'status': 'error',
                'message': 'Title is required'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING *;',
            (title, description)
        )
        new_task = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Task created successfully',
            'task': new_task
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to create task: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
