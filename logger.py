import logging
import sys
from datetime import datetime
import os

def setup_logger():
    """Set up application logging for production"""
    
    # Create logger
    logger = logging.getLogger("programmers_union")
    logger.setLevel(logging.INFO if not os.getenv('DEBUG') else logging.DEBUG)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # File handler for errors
    error_handler = logging.FileHandler('error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    
    return logger

# Global logger instance
app_logger = setup_logger()

def log_security_event(event_type: str, details: str, ip: str = "unknown"):
    """Log security-related events"""
    app_logger.warning(f"SECURITY EVENT - {event_type}: {details} (IP: {ip})")

def log_email_event(success: bool, recipient: str, error: str = None):
    """Log email sending events"""
    if success:
        app_logger.info(f"Email sent successfully to {recipient}")
    else:
        app_logger.error(f"Failed to send email to {recipient}: {error}")

def log_contact_inquiry(name: str, email: str, subject: str):
    """Log contact form submissions"""
    app_logger.info(f"New contact inquiry from {name} ({email}): {subject}")

def log_admin_action(action: str, username: str, ip: str = "unknown"):
    """Log admin panel actions"""
    app_logger.info(f"Admin action - {action} by {username} (IP: {ip})")