"""
Company Schemas
Pydantic models for company request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CompanyBase(BaseModel):
    """Base company schema"""
    name: str = Field(..., min_length=1, max_length=100)
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Schema for creating a company"""
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None


class CompanyUpdate(BaseModel):
    """Schema for updating a company"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None


class Company(CompanyBase):
    """Schema for company response"""
    id: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    logo_url: Optional[str] = None
    organization_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CompanyListResponse(BaseModel):
    """Schema for company list response"""
    companies: list[Company]
    total: int
    page: int
    page_size: int
