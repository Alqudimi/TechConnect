from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
import database
import models
import crud
from database import SessionLocal, engine
from email_service import send_contact_email
from auth import authenticate_user, create_access_token, require_admin, ACCESS_TOKEN_EXPIRE_MINUTES
import uvicorn
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Programmers Union", description="Professional Software Services Company")

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
    contact_data = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }
    
    # Save to database
    crud.create_contact_inquiry(db=db, **contact_data)
    
    # Send email notification
    email_sent = send_contact_email(
        from_name=name,
        from_email=email,
        subject=subject,
        message=message
    )
    
    if email_sent:
        success_message = "Thank you for your message! We'll get back to you soon. A confirmation email has been sent to your address."
    else:
        success_message = "Thank you for your message! We'll get back to you soon."
    
    return templates.TemplateResponse("contact.html", {
        "request": request, 
        "success": success_message
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
    if authenticate_user(username, password):
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
        return templates.TemplateResponse("admin/login.html", {
            "request": request, 
            "error": "Invalid credentials"
        })

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