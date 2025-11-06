"""
User Service - Microservices Architecture
Manages all user-related operations.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from models import db, User
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'user-service'}), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users."""
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    } for user in users]), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID."""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.json
    
    # Validate required fields
    if not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Username and email are required'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({'error': 'User with this username or email already exists'}), 409
    
    user = User(
        username=data['username'],
        email=data['email']
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user."""
    user = User.query.get_or_404(user_id)
    data = request.json
    
    if 'username' in data:
        # Check if username is already taken
        existing = User.query.filter(
            User.username == data['username'],
            User.id != user_id
        ).first()
        if existing:
            return jsonify({'error': 'Username already taken'}), 409
        user.username = data['username']
    
    if 'email' in data:
        # Check if email is already taken
        existing = User.query.filter(
            User.email == data['email'],
            User.id != user_id
        ).first()
        if existing:
            return jsonify({'error': 'Email already taken'}), 409
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/api/users/by-username/<username>', methods=['GET'])
def get_user_by_username(username):
    """Get a user by username."""
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/users/by-email/<email>', methods=['GET'])
def get_user_by_email(email):
    """Get a user by email."""
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/users/validate', methods=['POST'])
def validate_users():
    """Validate multiple user IDs exist. Used by other services."""
    data = request.json
    user_ids = data.get('user_ids', [])
    
    users = User.query.filter(User.id.in_(user_ids)).all()
    found_ids = [user.id for user in users]
    missing_ids = [uid for uid in user_ids if uid not in found_ids]
    
    return jsonify({
        'valid': len(missing_ids) == 0,
        'found_ids': found_ids,
        'missing_ids': missing_ids
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

