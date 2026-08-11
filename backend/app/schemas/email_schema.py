"""
Email Schemas
Pydantic models for email request/response validation
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
import json
from app.models.email_model import EmailStatus


class EmailBase(BaseModel):
    """Base email schema"""
    subject: str = Field(..., min_length=1, max_length=500)
    body: str = Field(..., min_length=1)
    body_html: Optional[str] = None
    to_email: EmailStr
    to_name: Optional[str] = None
    cc_email: Optional[EmailStr] = None
    bcc_email: Optional[EmailStr] = None
    from_email: EmailStr
    from_name: Optional[str] = None


class EmailCreate(EmailBase):
    """Schema for creating an email"""
    lead_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    template_id: Optional[str] = None


class EmailUpdate(BaseModel):
    """Schema for updating an email"""
    subject: Optional[str] = Field(None, min_length=1, max_length=500)
    body: Optional[str] = Field(None, min_length=1)
    body_html: Optional[str] = None
    to_email: Optional[EmailStr] = None
    to_name: Optional[str] = None
    cc_email: Optional[EmailStr] = None
    bcc_email: Optional[EmailStr] = None
    status: Optional[EmailStatus] = None


class Email(EmailBase):
    """Schema for email response"""
    id: str
    status: EmailStatus
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    tracking_id: Optional[str] = None
    opened_count: int
    clicked_count: int
    lead_id: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    organization_id: str
    created_by_id: Optional[str] = None
    template_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class EmailTemplateBase(BaseModel):
    """Base email template schema"""
    name: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=1, max_length=500)
    body: str = Field(..., min_length=1)
    body_html: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    variables: Optional[List[str]] = None


class EmailTemplateCreate(EmailTemplateBase):
    """Schema for creating an email template"""
    pass


class EmailTemplateUpdate(BaseModel):
    """Schema for updating an email template"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    subject: Optional[str] = Field(None, min_length=1, max_length=500)
    body: Optional[str] = Field(None, min_length=1)
    body_html: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None


class EmailTemplate(EmailTemplateBase):
    """Schema for email template response"""
    id: str
    organization_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @field_validator('variables', mode='before')
    @classmethod
    def parse_variables(cls, v):
        """Parse JSON string to list if needed"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
    
    model_config = ConfigDict(from_attributes=True)


class EmailListResponse(BaseModel):
    """Schema for email list response"""
    emails: List[Email]
    total: int
    page: int
    page_size: int


class EmailTemplateListResponse(BaseModel):
    """Schema for email template list response"""
    templates: List[EmailTemplate]
    total: int
    page: int
    page_size: int
