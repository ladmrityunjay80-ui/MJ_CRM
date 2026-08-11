"""
Lead Schemas
Pydantic models for lead request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.lead import LeadStatus, LeadSource


class LeadBase(BaseModel):
    """Base lead schema"""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema for creating a lead"""
    source: Optional[LeadSource] = LeadSource.OTHER
    estimated_value: Optional[float] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    assigned_to_id: Optional[str] = None
    contact_id: Optional[str] = None


class LeadUpdate(BaseModel):
    """Schema for updating a lead"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[LeadStatus] = None
    source: Optional[LeadSource] = None
    estimated_value: Optional[float] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    assigned_to_id: Optional[str] = None
    contact_id: Optional[str] = None


class Lead(LeadBase):
    """Schema for lead response"""
    id: str
    status: LeadStatus
    source: LeadSource
    estimated_value: Optional[float] = None
    probability: Optional[int] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    organization_id: str
    assigned_to_id: Optional[str] = None
    contact_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LeadListResponse(BaseModel):
    """Schema for lead list response"""
    leads: list[Lead]
    total: int
    page: int
    page_size: int
