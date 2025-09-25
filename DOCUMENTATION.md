# Programmers Union - Technical Documentation

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│   (Templates)   │◄──►│   (FastAPI)     │◄──►│   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐               │
         │              │     Email       │               │
         └──────────────►│   (SMTP/Gmail)  │               │
                        └─────────────────┘               │
                                 │                        │
                        ┌─────────────────┐               │
                        │    Logging      │               │
                        │  (File + Console)│◄──────────────┘
                        └─────────────────┘
```

### Component Interaction Flow

1. **User Request** → FastAPI routes
2. **Authentication** → JWT validation + rate limiting
3. **Input Processing** → Validation + sanitization
4. **Database Operations** → SQLAlchemy ORM
5. **Email Notifications** → SMTP with Gmail
6. **Logging** → Security events + audit trails
7. **Response** → Jinja2 templates + security headers

## 🛠️ Technical Implementation

### Authentication Flow

```python
# Complete authentication workflow
def authenticate_user(username: str, password: str, request: Request) -> bool:
    1. Extract client IP for rate limiting
    2. Check rate limit (5 attempts, 15-min lockout)
    3. Verify credentials against bcrypt hash
    4. Log security events (success/failure)
    5. Return authentication result
```

### Contact Form Processing

```python
# Contact form data flow
def submit_contact():
    1. Validate input (email format, length limits)
    2. Sanitize content (XSS prevention)
    3. Save to database (SQLite via SQLAlchemy)
    4. Send notifications (customer + admin emails)
    5. Log inquiry and email status
    6. Return user-friendly response
```

### Security Implementation

```python
# Multi-layer security approach
Security Layers:
├── Input Validation (regex, length checks)
├── SQL Injection Prevention (parameterized queries)
├── XSS Protection (content sanitization)
├── CSRF Protection (secure cookies)
├── Rate Limiting (IP-based throttling)
├── Authentication (JWT + bcrypt)
└── Security Headers (HSTS, CSP, etc.)
```

## 📊 Database Schema

### Contact Inquiries Table

```sql
CREATE TABLE contact_inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    subject VARCHAR NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_resolved BOOLEAN DEFAULT FALSE
);

-- Indexes for performance
CREATE INDEX idx_contact_email ON contact_inquiries(email);
CREATE INDEX idx_contact_created ON contact_inquiries(created_at);
```

### Database Operations

```python
# CRUD Operations
class ContactInquiry:
    - create_contact_inquiry()    # INSERT new inquiry
    - get_contact_inquiries()     # SELECT with pagination
    - delete_contact_inquiry()    # DELETE by ID
    
# Connection Management
- SessionLocal: SQLAlchemy session factory
- get_db(): Dependency injection for DB sessions
- Automatic connection cleanup and error handling
```

## 🔐 Security Specifications

### Password Security

```python
# Bcrypt Configuration
- Scheme: bcrypt (industry standard)
- Salt rounds: Automatic (random salt per password)
- Hash storage: Secure environment variables only
- Verification: Constant-time comparison
```

### JWT Token Security

```python
# Token Configuration
- Algorithm: HS256 (HMAC with SHA-256)
- Expiration: 30 minutes (configurable)
- Claims: username, expiration timestamp
- Storage: HTTP-only secure cookies
```

### Rate Limiting Algorithm

```python
# Rate Limiting Implementation
Rate Limit Rules:
├── Max Attempts: 5 failed login attempts per IP
├── Time Window: 15-minute lockout period
├── Storage: In-memory dictionary (IP → attempts)
├── Cleanup: Automatic cleanup of expired entries
└── Bypass: Successful login resets attempt counter
```

## 📧 Email System Architecture

### SMTP Configuration

```python
# Gmail SMTP Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # STARTTLS
AUTHENTICATION = "Gmail App Password"
ENCRYPTION = "TLS (Transport Layer Security)"
```

### Email Templates

```python
# Email Template System
Templates:
├── Admin Notification
│   ├── Subject: "New Contact Form Submission: {subject}"
│   ├── Content: Customer details + message
│   └── Metadata: Automatic timestamp + source
└── Customer Confirmation
    ├── Subject: "Thank you for contacting Programmers Union"
    ├── Content: Professional acknowledgment
    └── Auto-reply: "Do not reply to this email"
```

### Error Handling

```python
# Email Delivery Error Handling
Try-Catch Flow:
├── SMTP Connection → Log connection failures
├── Authentication → Log credential issues
├── Message Sending → Log delivery failures
├── Server Response → Log SMTP error codes
└── Graceful Degradation → Continue without email if failed
```

## 🔍 Logging & Monitoring

### Log Levels & Categories

```python
# Logging Configuration
Log Levels:
├── INFO: Normal operations (contact forms, admin logins)
├── WARNING: Security events (failed logins, rate limits)
├── ERROR: System errors (email failures, database issues)
└── DEBUG: Detailed troubleshooting (development only)

Log Categories:
├── Security Events: Authentication, rate limiting
├── Admin Actions: Dashboard access, inquiry management
├── Contact Inquiries: Form submissions, email status
└── System Errors: Exceptions, stack traces
```

### Log Format & Storage

```python
# Log Entry Format
'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Example: "2025-09-25 21:17:10 - programmers_union - INFO - New contact inquiry"

Storage Locations:
├── Console Output: Real-time monitoring
├── Error Log File: Persistent error tracking (error.log)
└── Structured Data: JSON format for log analysis
```

## 🚀 Performance Optimization

### Caching Strategy

```python
# HTTP Caching Headers
Static Files (CSS/JS):
├── Cache-Control: "public, max-age=3600" (1 hour)
├── ETag: Automatic file versioning
└── Compression: Gzip encoding

Dynamic Content:
├── Cache-Control: "no-cache, no-store, must-revalidate"
├── Pragma: "no-cache"
└── Expires: "0"
```

### Database Optimization

```python
# Performance Features
Database Optimizations:
├── Connection Pooling: SQLAlchemy session management
├── Query Optimization: Indexed columns for frequent searches
├── Pagination: LIMIT/OFFSET for large result sets
└── Connection Cleanup: Automatic session disposal
```

### Memory Management

```python
# Memory Optimization
Memory Usage:
├── Rate Limiting: In-memory storage with automatic cleanup
├── Session Management: Secure cookie storage (client-side)
├── Database Connections: Pool management with limits
└── Log Rotation: Automatic old log cleanup
```

## 🔧 Configuration Management

### Environment Variables

```python
# Required Configuration
REQUIRED_VARS = {
    'SESSION_SECRET': 'JWT signing key (minimum 32 characters)',
    'ADMIN_USERNAME': 'Admin login username',
    'ADMIN_PASSWORD': 'Strong admin password',
    'SMTP_EMAIL': 'Gmail address for sending emails',
    'SMTP_PASSWORD': 'Gmail App Password',
    'ADMIN_EMAIL': 'Email for receiving notifications'
}

# Optional Configuration
OPTIONAL_VARS = {
    'DEBUG': 'Enable debug mode (default: false)',
    'JWT_EXPIRATION_MINUTES': 'Session timeout (default: 30)',
    'MAX_LOGIN_ATTEMPTS': 'Rate limit threshold (default: 5)',
    'LOGIN_LOCKOUT_MINUTES': 'Lockout duration (default: 15)'
}
```

### Security Configuration

```python
# Security Settings
class SecurityConfig:
    JWT_ALGORITHM = "HS256"
    COOKIE_SETTINGS = {
        'httponly': True,    # Prevent XSS access
        'secure': True,      # HTTPS only
        'samesite': 'strict' # CSRF protection
    }
    
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': 'default-src \'self\'; ...'
    }
```

## 🧪 Testing Framework

### Manual Testing Procedures

```bash
# Contact Form Testing
# Valid submission test
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Test User&email=test@example.com&subject=Test&message=Test message"

# Invalid email test
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Test&email=invalid-email&subject=Test&message=Test"

# XSS injection test
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=<script>alert('xss')</script>&email=test@example.com&subject=Test&message=Test"
```

### Security Testing

```bash
# Rate Limiting Test
for i in {1..6}; do
  curl -X POST http://localhost:5000/admin/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=wronguser&password=wrongpass"
done

# Admin Authentication Test
curl -X POST http://localhost:5000/admin/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$ADMIN_USERNAME&password=$ADMIN_PASSWORD"
```

## 🔄 Deployment Pipeline

### Local Development

```bash
# Development Workflow
1. Clone repository
2. Set environment variables
3. Install dependencies: uv sync
4. Run application: uv run python main.py
5. Test functionality
6. Review logs for errors
```

### Production Deployment (Replit)

```python
# Deployment Configuration
Deployment Settings:
├── Target: autoscale (serverless)
├── Runtime: uv run python main.py
├── Host: 0.0.0.0:5000
├── Environment: Production secrets
└── Scaling: Automatic based on traffic
```

### Health Checks

```python
# Application Health Monitoring
Health Check Endpoints:
├── GET /: Homepage availability
├── Database: SQLite file accessibility
├── Email: SMTP connection test
└── Environment: Required variables validation
```

## 🐛 Troubleshooting Guide

### Common Error Patterns

```python
# Error Categories & Solutions
Authentication Errors:
├── "Invalid credentials" → Check ADMIN_USERNAME/PASSWORD
├── "Too many attempts" → Wait 15 minutes or check IP
└── "Token expired" → Re-login to get new JWT token

Email Errors:
├── "SMTP credentials not configured" → Set SMTP_EMAIL/PASSWORD
├── "Authentication failed" → Verify Gmail App Password
└── "Connection timeout" → Check network/firewall settings

Database Errors:
├── "Database locked" → Check file permissions
├── "Table doesn't exist" → Database auto-created on startup
└── "Disk full" → Check available storage space
```

### Log Analysis

```python
# Log Pattern Analysis
Error Patterns to Monitor:
├── "SECURITY EVENT" → Failed login attempts, rate limiting
├── "Failed to send email" → Email delivery issues
├── "Unexpected error" → Application exceptions
└── "Admin action" → Administrative activities
```

## 📈 Monitoring & Maintenance

### Performance Metrics

```python
# Key Performance Indicators
Metrics to Monitor:
├── Response Time: Page load speeds
├── Error Rate: Failed requests percentage
├── Email Delivery: Success/failure rates
├── Security Events: Failed login attempts
└── Database Performance: Query execution times
```

### Maintenance Schedule

```python
# Regular Maintenance Tasks
Daily:
├── Monitor error logs
├── Check email delivery status
└── Review security events

Weekly:
├── Database cleanup (old inquiries)
├── Log file rotation
└── Performance review

Monthly:
├── Security audit
├── Dependency updates
└── Backup verification
```

---

**Technical Documentation v1.0**  
*Last updated: September 2025*  
*Programmers Union - Professional Software Services*