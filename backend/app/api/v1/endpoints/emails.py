"""
Email Endpoints
CRUD operations for email communications
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from datetime import datetime
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.email_schema import EmailCreate, EmailUpdate, Email, EmailTemplateCreate, EmailTemplateUpdate, EmailTemplate, EmailListResponse, EmailTemplateListResponse
from app.models.user import User as UserModel
from app.models.email_model import Email as EmailModel, EmailTemplate as EmailTemplateModel
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=Email, status_code=status.HTTP_201_CREATED)
def create_email(
    email_data: EmailCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new email"""
    new_email = EmailModel(
        id=str(uuid.uuid4()),
        subject=email_data.subject,
        body=email_data.body,
        body_html=email_data.body_html,
        to_email=email_data.to_email,
        to_name=email_data.to_name,
        cc_email=email_data.cc_email,
        bcc_email=email_data.bcc_email,
        from_email=email_data.from_email or settings.SMTP_FROM,
        from_name=email_data.from_name,
        status="draft",
        tracking_id=str(uuid.uuid4()),
        opened_count="0",
        clicked_count="0",
        lead_id=email_data.lead_id,
        contact_id=email_data.contact_id,
        deal_id=email_data.deal_id,
        organization_id=current_user.organization_id,
        created_by_id=current_user.id,
        template_id=email_data.template_id
    )
    
    db.add(new_email)
    db.commit()
    db.refresh(new_email)
    
    return new_email


@router.get("/", response_model=EmailListResponse)
def get_emails(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all emails with filtering and pagination"""
    # Build query
    query = db.query(EmailModel).filter(EmailModel.organization_id == current_user.organization_id)
    
    # Apply filters
    if status:
        query = query.filter(EmailModel.status == status)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    emails = query.order_by(EmailModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "emails": emails,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{email_id}", response_model=Email)
def get_email(
    email_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific email"""
    email = db.query(EmailModel).filter(
        EmailModel.id == email_id,
        EmailModel.organization_id == current_user.organization_id
    ).first()
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    return email


@router.put("/{email_id}", response_model=Email)
def update_email(
    email_id: str,
    email_data: EmailUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update an email"""
    email = db.query(EmailModel).filter(
        EmailModel.id == email_id,
        EmailModel.organization_id == current_user.organization_id
    ).first()
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    # Update email fields
    update_data = email_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(email, field, value)
    
    db.commit()
    db.refresh(email)
    
    return email


@router.post("/{email_id}/send", response_model=Email)
def send_email(
    email_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Send an email"""
    email = db.query(EmailModel).filter(
        EmailModel.id == email_id,
        EmailModel.organization_id == current_user.organization_id
    ).first()
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    if email.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email has already been sent"
        )
    
    # TODO: Implement actual email sending logic using SMTP
    # For now, just mark as sent
    email.status = "sent"
    email.sent_at = datetime.utcnow()
    
    db.commit()
    db.refresh(email)
    
    return email


@router.delete("/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email(
    email_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete an email"""
    email = db.query(EmailModel).filter(
        EmailModel.id == email_id,
        EmailModel.organization_id == current_user.organization_id
    ).first()
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    db.delete(email)
    db.commit()
    
    return None


# Email Template Endpoints

@router.post("/templates/", response_model=EmailTemplate, status_code=status.HTTP_201_CREATED)
def create_email_template(
    template_data: EmailTemplateCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new email template"""
    new_template = EmailTemplateModel(
        id=str(uuid.uuid4()),
        name=template_data.name,
        subject=template_data.subject,
        body=template_data.body,
        body_html=template_data.body_html,
        description=template_data.description,
        category=template_data.category,
        variables=json.dumps(template_data.variables) if template_data.variables else None,
        organization_id=current_user.organization_id,
        is_active=True
    )
    
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    
    return new_template


@router.get("/templates/", response_model=EmailTemplateListResponse)
def get_email_templates(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all email templates with filtering and pagination"""
    # Build query
    query = db.query(EmailTemplateModel).filter(
        EmailTemplateModel.organization_id == current_user.organization_id,
        EmailTemplateModel.is_active == True
    )
    
    # Apply filters
    if category:
        query = query.filter(EmailTemplateModel.category == category)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    templates = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "templates": templates,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/templates/{template_id}", response_model=EmailTemplate)
def get_email_template(
    template_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get a specific email template"""
    template = db.query(EmailTemplateModel).filter(
        EmailTemplateModel.id == template_id,
        EmailTemplateModel.organization_id == current_user.organization_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email template not found"
        )
    
    return template


@router.put("/templates/{template_id}", response_model=EmailTemplate)
def update_email_template(
    template_id: str,
    template_data: EmailTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update an email template"""
    template = db.query(EmailTemplateModel).filter(
        EmailTemplateModel.id == template_id,
        EmailTemplateModel.organization_id == current_user.organization_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email template not found"
        )
    
    # Update template fields
    update_data = template_data.model_dump(exclude_unset=True)
    
    if "variables" in update_data and update_data["variables"] is not None:
        update_data["variables"] = json.dumps(update_data["variables"])
    
    for field, value in update_data.items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email_template(
    template_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Delete an email template"""
    template = db.query(EmailTemplateModel).filter(
        EmailTemplateModel.id == template_id,
        EmailTemplateModel.organization_id == current_user.organization_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email template not found"
        )
    
    db.delete(template)
    db.commit()
    
    return None
