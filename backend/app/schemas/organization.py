"""
Organization Schemas
Pydantic models for organization request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class OrganizationBase(BaseModel):
    """Base organization schema"""
    name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = None
    website: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """Schema for creating an organization"""
    slug: str = Field(..., min_length=3, max_length=50)
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    industry: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None


class Organization(OrganizationBase):
    """Schema for organization response"""
    id: str
    slug: str
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
