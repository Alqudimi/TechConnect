import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def send_contact_email(
    from_name: str,
    from_email: str,
    subject: str,
    message: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587
) -> bool:
    """Send contact form email via SMTP"""
    
    # Get SMTP credentials from environment
    smtp_email = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    admin_email = os.environ.get('ADMIN_EMAIL', smtp_email)
    print(f'SMTP_EMAIL: {smtp_email}\nSMTP_PASSWORD: {smtp_password}\nADMIN_EMAIL: {admin_email}\nport:{smtp_port}\nserver:{smtp_server} ')
    if not smtp_email or not smtp_password:
        print("SMTP credentials not configured")
        return False
    
    try:
        # Create message for admin notification
        admin_msg = MIMEMultipart()
        admin_msg['From'] = smtp_email
        admin_msg['To'] = admin_email
        admin_msg['Subject'] = f"New Contact Form Submission: {subject}"
        
        admin_body = f"""
New contact form submission from Programmers Union website:

Name: {from_name}
Email: {from_email}
Subject: {subject}

Message:
{message}

---
This email was sent automatically from the Programmers Union contact form.
        """
        
        admin_msg.attach(MIMEText(admin_body, 'plain'))
        
        # Create confirmation message for customer
        customer_msg = MIMEMultipart()
        customer_msg['From'] = smtp_email
        customer_msg['To'] = from_email
        customer_msg['Subject'] = "Thank you for contacting Programmers Union"
        
        customer_body = f"""
Dear {from_name},

Thank you for contacting Programmers Union! We have received your message and will get back to you within 24 hours.

Your message details:
Subject: {subject}
Message: {message}

Best regards,
The Programmers Union Team

---
This is an automated confirmation email. Please do not reply to this email.
        """
        
        customer_msg.attach(MIMEText(customer_body, 'plain'))
        
        # Send emails
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        
        # Send admin notification
        server.send_message(admin_msg)
        
        # Send customer confirmation
        server.send_message(customer_msg)
        
        server.quit()
        return True
        
    except Exception as e:
        from logger import app_logger
        app_logger.error(f"Failed to send email: {str(e)}")
        print(f"Failed to send email: {e}")
        return False
