"""
Main application entry point for Layered Monolith (MVC) architecture.
"""
from flask import Flask
from config import Config
from models import db
from routes import register_routes

def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Register routes
    register_routes(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

