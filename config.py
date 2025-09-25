import os
from typing import Optional

class Settings:
    # Database
    DATABASE_URL = "sqlite:///./programmers_union.db"
    
    # Security
    SESSION_SECRET: str = os.environ.get('SESSION_SECRET', '')
    if not SESSION_SECRET:
        raise ValueError("SESSION_SECRET environment variable must be set")
    
    # For development, provide fallback values - CHANGE THESE IN PRODUCTION!
    ADMIN_USERNAME: str = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD: str = os.environ.get('ADMIN_PASSWORD', 'temp_password_123')  # Change this!
    
    # JWT Configuration
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_MINUTES = 30
    
    # Security Headers
    SECURE_COOKIES = True
    HTTPS_ONLY = True
    
    # Email
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_EMAIL: Optional[str] = os.environ.get('SMTP_EMAIL', 'noreply@example.com')  # Change this!
    SMTP_PASSWORD: Optional[str] = os.environ.get('SMTP_PASSWORD', 'temp_password')  # Change this!
    ADMIN_EMAIL: Optional[str] = os.environ.get('ADMIN_EMAIL', 'admin@example.com')  # Change this!
    
    # Application
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    HOST = "0.0.0.0"
    PORT = 5000
    
    # Rate Limiting
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_LOCKOUT_MINUTES = 15
    
    # Contact Information
    COMPANY_EMAIL: str = os.environ.get('COMPANY_EMAIL', 'info@programmersunion.com')
    COMPANY_PHONE: str = os.environ.get('COMPANY_PHONE', '+1 (555) 123-4567') 
    COMPANY_ADDRESS: str = os.environ.get('COMPANY_ADDRESS', '123 Tech Street')
    COMPANY_CITY: str = os.environ.get('COMPANY_CITY', 'Digital City, DC 12345')

settings = Settings()