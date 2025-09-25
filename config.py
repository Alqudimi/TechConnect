import os
from typing import Optional

class Settings:
    # Database
    DATABASE_URL = "sqlite:///./programmers_union.db"
    
    # Security
    SESSION_SECRET: str = os.environ.get('SESSION_SECRET')
    if not SESSION_SECRET:
        raise ValueError("SESSION_SECRET environment variable must be set")
    
    ADMIN_USERNAME: str = os.environ.get('ADMIN_USERNAME')
    if not ADMIN_USERNAME:
        raise ValueError("ADMIN_USERNAME environment variable must be set")
    
    ADMIN_PASSWORD: str = os.environ.get('ADMIN_PASSWORD')
    if not ADMIN_PASSWORD:
        raise ValueError("ADMIN_PASSWORD environment variable must be set")
    
    # JWT Configuration
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_MINUTES = 30
    
    # Security Headers
    SECURE_COOKIES = True
    HTTPS_ONLY = True
    
    # Email
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_EMAIL: Optional[str] = os.environ.get('SMTP_EMAIL')
    SMTP_PASSWORD: Optional[str] = os.environ.get('SMTP_PASSWORD')
    ADMIN_EMAIL: Optional[str] = os.environ.get('ADMIN_EMAIL')
    
    # Application
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    HOST = "0.0.0.0"
    PORT = 5000
    
    # Rate Limiting
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_LOCKOUT_MINUTES = 15

settings = Settings()