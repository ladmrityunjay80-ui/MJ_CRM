"""
Contact Schemas
Pydantic models for contact request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ContactBase(BaseModel):
    """Base contact schema"""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None


class ContactCreate(ContactBase):
    """Schema for creating a contact"""
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    company_id: Optional[str] = None


class ContactUpdate(BaseModel):
    """Schema for updating a contact"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    company_id: Optional[str] = None


class Contact(ContactBase):
    """Schema for contact response"""
    id: str
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    avatar_url: Optional[str] = None
    organization_id: str
    company_id: Optional[str] = None
    created_by_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ContactListResponse(BaseModel):
    """Schema for contact list response"""
    contacts: list[Contact]
    total: int
    page: int
    page_size: int
