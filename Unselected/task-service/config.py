"""
Configuration for Task Service.
"""
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'task-service-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///task_service.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5001')
    USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')

