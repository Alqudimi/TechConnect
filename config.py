import os

class Settings:
    # Database
    DATABASE_URL = "sqlite:///./programmers_union.db"
    
    # Security
    SESSION_SECRET = os.environ.get('SESSION_SECRET', 'change-this-in-production')
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"  # Change in production
    
    # Email
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_EMAIL = os.environ.get('SMTP_EMAIL', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', '')
    
    # Application
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 5000

settings = Settings()