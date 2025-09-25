from sqlalchemy.orm import Session
from models import ContactInquiry

def create_contact_inquiry(db: Session, name: str, email: str, subject: str, message: str):
    db_inquiry = ContactInquiry(
        name=name,
        email=email,
        subject=subject,
        message=message
    )
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry

def get_contact_inquiries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ContactInquiry).offset(skip).limit(limit).all()

def delete_contact_inquiry(db: Session, inquiry_id: int):
    inquiry = db.query(ContactInquiry).filter(ContactInquiry.id == inquiry_id).first()
    if inquiry:
        db.delete(inquiry)
        db.commit()
    return inquiry