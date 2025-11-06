"""
Configuration for User Service.
"""
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'user-service-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///user_service.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

