# Programmers Union - Professional Software Services Website

## 🚀 Overview

Programmers Union is a production-ready FastAPI-based website for a professional software development company. The platform features a modern web presence with service information, portfolio showcase, secure contact functionality, and an admin panel for managing customer inquiries.

## ✨ Features

### **Public Website**
- 🏠 **Home Page** - Company overview with modern design
- 🛠️ **Services Page** - Detailed service offerings (Web Development, Mobile Apps, Cloud Solutions)
- 💼 **Portfolio Showcase** - Project demonstrations and case studies
- 👥 **About Us** - Company information and team details
- 📞 **Contact Form** - Professional contact system with email notifications

### **Admin Panel**
- 🔐 **Secure Authentication** - JWT-based login with bcrypt password hashing
- 📊 **Dashboard** - View and manage customer inquiries
- 🗑️ **Inquiry Management** - Delete processed inquiries
- 🔒 **Session Management** - Secure cookie-based sessions with 30-minute timeout

### **Security Features**
- 🛡️ **Rate Limiting** - Protection against brute force attacks (5 attempts, 15-minute lockout)
- 🔍 **Input Validation** - Comprehensive sanitization against XSS and injection attacks
- 📧 **Email Security** - SMTP with TLS encryption using Gmail App Passwords
- 🚦 **Security Headers** - HSTS, CSP, X-Frame-Options, and more
- 📝 **Audit Logging** - Security events, failed logins, and admin actions tracking

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt hashing
- **Email**: SMTP with Gmail integration
- **Frontend**: Jinja2 templates with responsive CSS
- **Security**: Comprehensive headers and input validation
- **Logging**: Structured logging with file and console output
- **Package Management**: uv (modern Python package manager)

## 📋 Prerequisites

- Python 3.11+
- Gmail account with App Password enabled
- Basic understanding of FastAPI and web development

## 🚀 Quick Start

### 1. Environment Setup

Create the following environment variables in Replit Secrets or your `.env` file:

```bash
# Security (Required)
SESSION_SECRET=your-strong-secret-key-here

# Admin Credentials (Required)
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-strong-password

# Email Configuration (Required for contact form)
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
ADMIN_EMAIL=admin@yourdomain.com

# Optional
DEBUG=false
```

### 2. Installation

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py
```

### 3. Access the Application

- **Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

## 📧 Email Configuration

### Gmail App Password Setup

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to Security → 2-Step Verification
3. Scroll down to "App passwords"
4. Generate a new app password for "Programmers Union Website"
5. Use the 16-character password as `SMTP_PASSWORD`

### Email Features

- **Customer Confirmation**: Automatic confirmation emails to form submitters
- **Admin Notifications**: Instant notifications for new inquiries
- **Professional Templates**: Branded email templates with company information
- **Error Handling**: Graceful degradation if email service is unavailable

## 🗂️ Project Structure

```
programmers-union/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration and environment variables
├── auth.py                 # Authentication and security functions
├── database.py             # Database connection and session management
├── models.py               # SQLAlchemy database models
├── crud.py                 # Database CRUD operations
├── email_service.py        # Email notification service
├── logger.py               # Logging configuration and functions
├── templates/              # Jinja2 HTML templates
│   ├── admin/             # Admin panel templates
│   │   ├── dashboard.html
│   │   └── login.html
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── services.html      # Services page
│   ├── portfolio.html     # Portfolio page
│   ├── about.html         # About page
│   └── contact.html       # Contact page
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       ├── main.js        # Main JavaScript
│       └── admin.js       # Admin panel JavaScript
├── programmers_union.db   # SQLite database
├── pyproject.toml         # Python dependencies
├── replit.md             # Project documentation
└── README.md             # This file
```

## 🔒 Security Features

### Authentication & Authorization
- **Secure Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure session management
- **Rate Limiting**: IP-based brute force protection
- **Session Timeout**: Automatic logout after 30 minutes

### Input Validation
- **Email Validation**: RFC-compliant email format checking
- **Text Sanitization**: XSS prevention and input cleaning
- **Length Limits**: Prevent buffer overflow attacks
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy

### Security Headers
- **HSTS**: Enforce HTTPS connections
- **CSP**: Content Security Policy
- **X-Frame-Options**: Clickjacking protection
- **X-Content-Type-Options**: MIME type sniffing protection

## 📊 Monitoring & Logging

### Log Types
- **Security Events**: Failed logins, rate limiting triggers
- **Admin Actions**: Dashboard access, inquiry deletions
- **Contact Inquiries**: Form submissions and email status
- **System Errors**: Detailed error tracking with stack traces

### Log Locations
- **Console Output**: Real-time application logs
- **Error Log File**: `error.log` for persistent error tracking
- **Admin Actions**: Structured logging for audit trails

## 🚀 Deployment

### Development
```bash
uv run python main.py
```

### Production (Replit)
The application is configured for Replit deployment with:
- Host: `0.0.0.0`
- Port: `5000`
- Deployment Target: `autoscale`
- Run Command: `uv run python main.py`

### Environment Variables
Ensure all required environment variables are set in production:
- `SESSION_SECRET`: Strong random key for JWT signing
- `ADMIN_USERNAME`: Admin login username
- `ADMIN_PASSWORD`: Strong admin password
- `SMTP_EMAIL`: Gmail address for sending emails
- `SMTP_PASSWORD`: Gmail App Password
- `ADMIN_EMAIL`: Email to receive contact form notifications

## 🛠️ API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /services` - Services page
- `GET /portfolio` - Portfolio page
- `GET /about` - About page
- `GET /contact` - Contact form
- `POST /contact` - Submit contact form

### Admin Routes
- `GET /admin` - Admin login page
- `POST /admin/login` - Admin authentication
- `GET /admin/dashboard` - Admin dashboard (protected)
- `DELETE /admin/inquiry/{id}` - Delete inquiry (protected)
- `POST /admin/logout` - Admin logout

### Static Assets
- `/static/css/*` - Stylesheets
- `/static/js/*` - JavaScript files

## 🔧 Configuration Options

### Security Settings
```python
# config.py
JWT_EXPIRATION_MINUTES = 30    # Session timeout
MAX_LOGIN_ATTEMPTS = 5         # Rate limiting
LOGIN_LOCKOUT_MINUTES = 15     # Lockout duration
```

### Email Settings
```python
# config.py
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587                # TLS port
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Home page loads correctly
- [ ] All navigation links work
- [ ] Contact form accepts valid input
- [ ] Contact form rejects invalid input
- [ ] Email notifications are sent
- [ ] Admin login works with correct credentials
- [ ] Admin login blocks incorrect credentials
- [ ] Rate limiting activates after failed attempts
- [ ] Admin dashboard displays inquiries
- [ ] Inquiry deletion works
- [ ] Admin logout clears session

### Contact Form Testing
```bash
# Test valid submission
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Test User&email=test@example.com&subject=Test&message=Test message"

# Test invalid email
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Test&email=invalid-email&subject=Test&message=Test"
```

## 🐛 Troubleshooting

### Common Issues

**Email Not Sending**
- Verify Gmail App Password is correct
- Check `SMTP_EMAIL` and `SMTP_PASSWORD` environment variables
- Ensure 2-Step Verification is enabled on Gmail account

**Admin Login Fails**
- Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables
- Verify strong password meets security requirements
- Check if rate limiting is active (wait 15 minutes)

**Database Errors**
- Ensure SQLite file permissions are correct
- Check disk space availability
- Verify database file is not corrupted

**Environment Variables Not Found**
- Verify all required environment variables are set
- Check variable names for typos
- Restart application after adding variables

## 📈 Performance Considerations

- **Static File Caching**: 1-hour cache for CSS/JS files
- **Database Optimization**: Indexed columns for frequent queries
- **Memory Management**: Proper session cleanup and connection pooling
- **Rate Limiting**: In-memory storage (consider Redis for scaling)

## 🔄 Maintenance

### Regular Tasks
- Monitor error logs for unusual activity
- Review contact inquiries and respond promptly
- Update dependencies periodically
- Backup database regularly
- Rotate admin passwords quarterly

### Security Updates
- Monitor security advisories for FastAPI and dependencies
- Update Python and packages regularly
- Review and update security headers as needed
- Audit login attempts and security events

## 📞 Support

For technical support or customization requests:
- Contact: [Your contact information]
- Documentation: This README file
- Logs: Check `error.log` file for detailed error information

## 📄 License

[Specify your license here]

## 🤝 Contributing

[If open source, specify contribution guidelines]

---

**Built with ❤️ by Programmers Union**

*Last updated: September 2025*