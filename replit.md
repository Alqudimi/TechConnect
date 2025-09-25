# Programmers Union - Professional Software Services Company

## Overview
This is a production-ready FastAPI-based website for "Programmers Union" - a professional software development company. The application provides a modern web presence with service information, portfolio showcase, secure contact functionality, and an admin panel for managing customer inquiries.

## Project Status: ✅ PRODUCTION READY

### Security & Features Implemented
- ✅ **Enterprise-grade Security**: Rate limiting, input validation, security headers
- ✅ **Professional Email System**: SMTP integration with Gmail, dual notifications
- ✅ **Secure Authentication**: JWT tokens, bcrypt hashing, session management
- ✅ **Comprehensive Logging**: Security events, audit trails, error tracking
- ✅ **Production Configuration**: Environment variables, error handling
- ✅ **Database Security**: Parameterized queries, proper session management

## Project Architecture

### Technology Stack
- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT-based admin authentication with bcrypt password hashing
- **Email**: Professional SMTP service with Gmail integration
- **Frontend**: Jinja2 templates with responsive CSS and JavaScript
- **Security**: Multi-layer protection with rate limiting and input validation
- **Logging**: Structured logging with file and console output
- **Package Management**: uv (modern Python package manager)

### Project Structure
```
├── main.py              # FastAPI application entry point with security middleware
├── config.py            # Production configuration and environment variables
├── auth.py              # Authentication with rate limiting and security
├── database.py          # Database connection and session management
├── models.py            # SQLAlchemy database models
├── crud.py              # Database CRUD operations
├── email_service.py     # Professional email notification service
├── logger.py            # Comprehensive logging system
├── templates/           # Professional Jinja2 HTML templates
│   ├── admin/          # Secure admin panel templates
│   │   ├── dashboard.html
│   │   └── login.html
│   ├── base.html       # Base template with security headers
│   ├── index.html      # Modern home page
│   ├── services.html   # Professional services page
│   ├── portfolio.html  # Portfolio showcase
│   ├── about.html      # Company information
│   └── contact.html    # Secure contact form
├── static/             # Optimized static assets
│   ├── css/
│   │   └── style.css   # Professional responsive stylesheet
│   └── js/
│       ├── main.js     # Main JavaScript functionality
│       └── admin.js    # Admin panel interactions
├── programmers_union.db # SQLite database
├── pyproject.toml      # Python dependencies
├── README.md           # User documentation
├── DOCUMENTATION.md    # Technical documentation
└── replit.md          # This project overview
```

### Features
1. **Professional Website**:
   - Modern responsive home page with company branding
   - Detailed services page showcasing technical expertise
   - Portfolio section with project demonstrations
   - Professional about page with team information
   - Secure contact form with real-time validation

2. **Secure Admin Panel**:
   - Enterprise-grade JWT-based authentication
   - Rate limiting protection (5 attempts, 15-minute lockout)
   - Dashboard to view and manage customer inquiries
   - Secure inquiry deletion with audit logging
   - Session management with secure HTTP-only cookies

3. **Production Database**:
   - Contact inquiry storage with validation
   - Automatic timestamp tracking
   - Indexed columns for performance
   - Secure parameterized queries

4. **Professional Email System**:
   - Customer confirmation emails with branded templates
   - Admin notifications for new inquiries
   - SMTP with TLS encryption
   - Error handling and delivery logging

## Security Implementation

### Authentication & Authorization
- **Secure Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure session management with 30-minute timeout
- **Rate Limiting**: IP-based brute force protection
- **Session Security**: HTTP-only, secure, SameSite cookies

### Input Security
- **Email Validation**: RFC-compliant format checking
- **Content Sanitization**: XSS prevention with regex filtering
- **Length Validation**: Buffer overflow protection
- **SQL Injection Protection**: Parameterized queries only

### Infrastructure Security
- **Security Headers**: HSTS, CSP, X-Frame-Options, X-Content-Type-Options
- **Cache Control**: Proper caching for static vs dynamic content
- **Error Handling**: Graceful degradation without information disclosure
- **Audit Logging**: Security events and admin actions tracking

## Configuration

### Required Environment Variables
```bash
# Security (Required)
SESSION_SECRET=your-strong-secret-key-here

# Admin Credentials (Required)
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-strong-password

# Email Configuration (Required)
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
ADMIN_EMAIL=admin@yourdomain.com

# Optional Configuration
DEBUG=false
```

### Production Configuration
- **Host**: 0.0.0.0 (Replit environment)
- **Port**: 5000 (Replit requirement)
- **Database**: SQLite with performance optimization
- **Session Timeout**: 30 minutes
- **Rate Limiting**: 5 attempts per IP, 15-minute lockout
- **Email**: Professional SMTP with TLS encryption

## Development & Deployment

### Local Development
```bash
uv sync                    # Install dependencies
uv run python main.py     # Run application
```

### Production Deployment (Replit)
- **Deployment Target**: autoscale (serverless)
- **Run Command**: `uv run python main.py`
- **Environment**: Production secrets configured
- **Monitoring**: Comprehensive logging and error tracking

### Access Points
- **Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Production URL**: [Your Replit deployment URL]

## Monitoring & Maintenance

### Logging System
- **Security Events**: Failed logins, rate limiting, admin actions
- **Contact Inquiries**: Form submissions, email delivery status
- **System Errors**: Application exceptions with stack traces
- **Performance**: Request timing and database operations

### Health Monitoring
- **Database**: Connection health and query performance
- **Email**: SMTP connectivity and delivery rates
- **Security**: Failed authentication attempts and threats
- **Performance**: Response times and resource usage

## Recent Production Updates

- **2025-09-25**: Successfully imported and configured for Replit environment
- **Environment Setup**: Configured fallback values for development environment
- **Host Configuration**: Properly configured for Replit proxy (0.0.0.0:5000)
- **Workflow Setup**: Configured automated deployment with uvicorn server
- **Deployment Config**: Set up autoscale deployment target for production
- **Dependency Management**: All dependencies properly installed with uv package manager
- **Testing**: Verified all endpoints and core functionality working
- **Security**: Maintained enterprise-grade security with environment variables
- **Import Status**: ✅ SUCCESSFULLY COMPLETED - Ready for use

## User Preferences & Standards

- **Security First**: Enterprise-grade security implementation
- **Modern Tooling**: uv package management, FastAPI best practices
- **Professional Design**: Responsive templates with modern CSS
- **Real Functionality**: No mock data, actual email delivery
- **Production Ready**: Comprehensive error handling and monitoring
- **Documentation**: Complete technical and user documentation

## Deployment Status

### ✅ Production Checklist
- [x] Security vulnerabilities eliminated
- [x] Professional email functionality implemented
- [x] Secure authentication with rate limiting
- [x] Input validation and sanitization
- [x] Security headers and HTTPS configuration
- [x] Comprehensive logging and monitoring
- [x] Error handling and graceful degradation
- [x] Performance optimization
- [x] Professional documentation
- [x] Ready for customer use

**Status**: Ready for production deployment and customer traffic.

---

*Last updated: September 2025*  
*Programmers Union - Professional Software Services*