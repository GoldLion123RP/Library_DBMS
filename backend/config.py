import os

class Config:
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'LibraryDB')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')