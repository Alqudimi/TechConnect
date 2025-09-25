from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import time
from config import settings

# Security configuration
SECRET_KEY = settings.SESSION_SECRET
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_EXPIRATION_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Admin credentials from environment (secure)
ADMIN_USERNAME = settings.ADMIN_USERNAME
ADMIN_PASSWORD = settings.ADMIN_PASSWORD
ADMIN_PASSWORD_HASH = pwd_context.hash(ADMIN_PASSWORD)

# Rate limiting storage (in production, use Redis or database)
login_attempts: Dict[str, Dict[str, int]] = {}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return {"username": username}
    except JWTError:
        return None

def get_client_ip(request: Request) -> str:
    """Get client IP address for rate limiting"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def check_rate_limit(ip: str) -> bool:
    """Check if IP has exceeded rate limit for login attempts"""
    current_time = int(time.time())
    cleanup_old_attempts(current_time)
    
    if ip not in login_attempts:
        return True
        
    attempts = login_attempts[ip]
    if attempts["count"] >= settings.MAX_LOGIN_ATTEMPTS:
        lockout_end = attempts["last_attempt"] + (settings.LOGIN_LOCKOUT_MINUTES * 60)
        if current_time < lockout_end:
            return False
        else:
            # Reset after lockout period
            del login_attempts[ip]
            return True
    
    return True

def record_failed_attempt(ip: str):
    """Record a failed login attempt"""
    current_time = int(time.time())
    if ip not in login_attempts:
        login_attempts[ip] = {"count": 1, "last_attempt": current_time}
    else:
        login_attempts[ip]["count"] += 1
        login_attempts[ip]["last_attempt"] = current_time

def cleanup_old_attempts(current_time: int):
    """Clean up old login attempts to prevent memory leaks"""
    expired_ips = []
    for ip, attempts in login_attempts.items():
        if current_time - attempts["last_attempt"] > (settings.LOGIN_LOCKOUT_MINUTES * 60):
            expired_ips.append(ip)
    
    for ip in expired_ips:
        del login_attempts[ip]

def authenticate_user(username: str, password: str, request: Request) -> bool:
    """Authenticate a user with rate limiting"""
    client_ip = get_client_ip(request)
    
    # Check rate limit
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many failed attempts. Try again in {settings.LOGIN_LOCKOUT_MINUTES} minutes."
        )
    
    # Verify credentials
    if username == ADMIN_USERNAME and verify_password(password, ADMIN_PASSWORD_HASH):
        # Reset failed attempts on successful login
        if client_ip in login_attempts:
            del login_attempts[client_ip]
        return True
    else:
        # Record failed attempt
        record_failed_attempt(client_ip)
        return False

def get_current_user_from_cookie(request: Request) -> Optional[dict]:
    """Get current user from session cookie"""
    token = request.cookies.get("admin_token")
    if not token:
        return None
    return verify_token(token)

def require_admin(request: Request) -> dict:
    """Dependency to require admin authentication"""
    user = get_current_user_from_cookie(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user