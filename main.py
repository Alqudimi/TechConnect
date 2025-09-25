from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import database
import models
import crud
import re
from database import SessionLocal, engine
from email_service import send_contact_email
from auth import authenticate_user, create_access_token, require_admin, ACCESS_TOKEN_EXPIRE_MINUTES, get_client_ip
from logger import log_contact_inquiry, log_email_event, log_security_event, log_admin_action
import uvicorn
import os
from config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Programmers Union", description="Professional Software Services Company")

# Security middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'"
    
    # Cache control for static files
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=3600"
    else:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    
    return response

# Input validation functions
def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize and validate text input"""
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Input cannot be empty")
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text.strip())
    
    if len(sanitized) > max_length:
        raise HTTPException(status_code=400, detail=f"Input too long (max {max_length} characters)")
    
    return sanitized

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.post("/contact")
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Validate and sanitize inputs
        clean_name = sanitize_input(name, 100)
        clean_email = email.strip().lower()
        clean_subject = sanitize_input(subject, 200)
        clean_message = sanitize_input(message, 5000)
        
        # Validate email format
        if not validate_email(clean_email):
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        contact_data = {
            "name": clean_name,
            "email": clean_email,
            "subject": clean_subject,
            "message": clean_message
        }
        
        # Log the contact inquiry
        client_ip = get_client_ip(request)
        log_contact_inquiry(clean_name, clean_email, clean_subject)
        
        # Save to database
        crud.create_contact_inquiry(db=db, **contact_data)
        
        # Send email notification
        email_sent = send_contact_email(
            from_name=clean_name,
            from_email=clean_email,
            subject=clean_subject,
            message=clean_message
        )
        
        # Log email result
        log_email_event(email_sent, clean_email)
        
        if email_sent:
            success_message = "Thank you for your message! We'll get back to you soon. A confirmation email has been sent to your address."
        else:
            success_message = "Thank you for your message! We'll get back to you soon."
        
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "success": success_message
        })
    
    except HTTPException as e:
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": e.detail
        })
    except Exception as e:
        from logger import app_logger
        app_logger.error(f"Unexpected error in contact form: {str(e)}", exc_info=True)
        return templates.TemplateResponse("contact.html", {
            "request": request, 
            "error": "An error occurred while processing your request. Please try again."
        })

@app.get("/admin", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

@app.post("/admin/login")
async def admin_authenticate(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    client_ip = get_client_ip(request)
    
    try:
        if authenticate_user(username, password, request):
            log_admin_action("successful_login", username, client_ip)
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": username}, expires_delta=access_token_expires
            )
            response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)
            response.set_cookie(
                key="admin_token", 
                value=access_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
            return response
        else:
            log_security_event("failed_login_attempt", f"Username: {username}", client_ip)
            return templates.TemplateResponse("admin/login.html", {
                "request": request, 
                "error": "Invalid credentials"
            })
    except HTTPException as e:
        if e.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            log_security_event("rate_limit_triggered", f"Username: {username}", client_ip)
            return templates.TemplateResponse("admin/login.html", {
                "request": request, 
                "error": e.detail
            })
        raise e

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    inquiries = crud.get_contact_inquiries(db)
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request, 
        "inquiries": inquiries
    })

@app.delete("/admin/inquiry/{inquiry_id}")
async def delete_inquiry(
    inquiry_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    crud.delete_contact_inquiry(db, inquiry_id)
    return {"message": "Inquiry deleted successfully"}

@app.post("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="admin_token")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)