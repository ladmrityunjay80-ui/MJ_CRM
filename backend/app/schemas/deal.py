"""
Deal Schemas
Pydantic models for deal request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from app.models.deal import DealStage


class DealBase(BaseModel):
    """Base deal schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    value: float = Field(..., gt=0)
    currency: str = "USD"
    probability: Optional[int] = Field(None, ge=0, le=100)


class DealCreate(DealBase):
    """Schema for creating a deal"""
    expected_close_date: Optional[date] = None
    stage: Optional[DealStage] = DealStage.PROSPECTING
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    company_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    contact_id: Optional[str] = None


class DealUpdate(BaseModel):
    """Schema for updating a deal"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    value: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    stage: Optional[DealStage] = None
    lost_reason: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    company_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    contact_id: Optional[str] = None


class Deal(DealBase):
    """Schema for deal response"""
    id: str
    expected_close_date: Optional[date] = None
    actual_close_date: Optional[date] = None
    stage: DealStage
    lost_reason: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[list[str]] = None
    organization_id: str
    company_id: Optional[str] = None
    assigned_to_id: Optional[str] = None
    contact_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DealListResponse(BaseModel):
    """Schema for deal list response"""
    deals: list[Deal]
    total: int
    page: int
    page_size: int
