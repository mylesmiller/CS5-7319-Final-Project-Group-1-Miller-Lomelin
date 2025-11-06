"""
Configuration settings for the application.
"""
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///task_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

